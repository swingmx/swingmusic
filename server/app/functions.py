"""
This module contains functions for the server
"""
import datetime
import os
import time
from dataclasses import asdict
from io import BytesIO

import requests
from app import api, helpers, instances, models, settings
from app.lib import albumslib, folderslib, watchdoge
from app.lib.taglib import get_tags
from app.logger import Log
from PIL import Image
from progress.bar import Bar


@helpers.background
def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """

    while True:
        populate()
        fetch_artist_images()

        time.sleep(60)


@helpers.background
def start_watchdog():
    """
    Starts the file watcher.
    """
    watchdoge.watch.run()


def populate():
    """
    Populate the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to
    extract it.
    """
    start = time.time()
    db_tracks = instances.tracks_instance.get_all_tracks()
    tagged_tracks = []
    albums = []
    folders = set()

    files = helpers.run_fast_scandir(settings.HOME_DIR, [".flac", ".mp3"], full=True)[1]

    _bar = Bar("Checking files", max=len(files))
    for track in db_tracks:
        if track["filepath"] in files:
            files.remove(track["filepath"])
        _bar.next()

    _bar.finish()

    Log(f"Found {len(files)} untagged files")

    _bar = Bar("Tagging files", max=len(files))
    for file in files:
        tags = get_tags(file)
        foldername = os.path.dirname(file)
        folders.add(foldername)

        if tags is not None:
            tagged_tracks.append(tags)
            api.DB_TRACKS.append(tags)

        _bar.next()
    _bar.finish()

    Log(f"Tagged {len(tagged_tracks)} tracks")

    pre_albums = []

    for t in tagged_tracks:
        a = {
            "title": t["album"],
            "artist": t["albumartist"],
        }

        if a not in pre_albums:
            pre_albums.append(a)

    exist_count = 0
    _bar = Bar("Creating albums", max=len(pre_albums))
    for aa in pre_albums:
        albumindex = albumslib.find_album(aa["title"], aa["artist"])

        if albumindex is None:
            track = [
                track
                for track in tagged_tracks
                if track["album"] == aa["title"]
                and track["albumartist"] == aa["artist"]
            ][0]

            album = albumslib.create_album(track)
            api.ALBUMS.append(album)
            albums.append(album)

            instances.album_instance.insert_album(asdict(album))

        else:
            exist_count += 1

        _bar.next()

    _bar.finish()

    Log(f"{exist_count} of {len(albums)} were already in the database")

    _bar = Bar("Creating tracks", max=len(tagged_tracks))
    for track in tagged_tracks:
        try:
            album_index = albumslib.find_album(track["album"], track["albumartist"])
            album = api.ALBUMS[album_index]

            track["image"] = album.image
            upsert_id = instances.tracks_instance.insert_song(track)

            track["_id"] = {"$oid": str(upsert_id)}
            api.TRACKS.append(models.Track(track))
        except TypeError:
            # Bug: some albums are not found although they exist in `api.ALBUMS`. It has something to do with the bisection method used or sorting. Not sure yet.
            pass

        _bar.next()

    _bar.finish()

    Log(f"Added {len(tagged_tracks)} new tracks and {len(albums)} new albums")

    _bar = Bar("Creating folders", max=len(folders))
    for folder in folders:
        if folder not in api.VALID_FOLDERS:
            api.VALID_FOLDERS.add(folder)
            fff = folderslib.create_folder(folder)
            api.FOLDERS.append(fff)

        _bar.next()

    _bar.finish()

    Log(f"Created {len(api.FOLDERS)} folders")

    end = time.time()

    print(
        str(datetime.timedelta(seconds=round(end - start)))
        + " elapsed for "
        + str(len(files))
        + " files"
    )


def fetch_image_path(artist: str) -> str or None:
    """
    Returns a direct link to an artist image.
    """

    try:
        url = f"https://api.deezer.com/search/artist?q={artist}"
        response = requests.get(url)
        data = response.json()

        return data["data"][0]["picture_medium"]
    except requests.exceptions.ConnectionError:
        time.sleep(5)
        return None
    except (IndexError, KeyError):
        return None


def fetch_artist_images():
    """Downloads the artists images"""

    artists = []

    for song in api.DB_TRACKS:
        this_artists = song["artists"].split(", ")

        for artist in this_artists:
            if artist not in artists:
                artists.append(artist)

    _bar = Bar("Processing images", max=len(artists))
    for artist in artists:
        file_path = (
            helpers.app_dir + "/images/artists/" + artist.replace("/", "::") + ".webp"
        )

        if not os.path.exists(file_path):
            img_path = fetch_image_path(artist)

            if img_path is not None:
                try:
                    img = Image.open(BytesIO(requests.get(img_path).content))
                    img.save(file_path, format="webp")
                except requests.exceptions.ConnectionError:
                    time.sleep(5)

        _bar.next()

    _bar.finish()


def fetch_album_bio(title: str, albumartist: str):
    """
    Returns the album bio for a given album.
    """
    last_fm_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(
        settings.LAST_FM_API_KEY, albumartist, title
    )

    try:
        response = requests.get(last_fm_url)
        data = response.json()
    except:
        return None

    try:
        bio = data["album"]["wiki"]["summary"].split('<a href="https://www.last.fm/')[0]
    except KeyError:
        bio = None

    return bio
