"""
This module contains functions for the server
"""
from dataclasses import asdict
import datetime
import os
import random
import time
from io import BytesIO
from typing import List

import requests
from app import api
from app import helpers
from app import instances
from app import models
from app import settings
from app.lib import albumslib
from app.lib import folderslib
from app.lib import watchdoge
from PIL import Image
from progress.bar import Bar

from app.logger import Log
from app.lib.taglib import get_tags, return_album_art


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

    _bar = Bar("Creating stuff", max=len(tagged_tracks))
    for track in tagged_tracks:
        albumindex = albumslib.find_album(track["album"], track["albumartist"])
        album = None

        if albumindex is None:
            album = albumslib.create_album(track)
            api.ALBUMS.append(album)
            albums.append(album)
            instances.album_instance.insert_album(asdict(album))
        else:
            album = api.ALBUMS[albumindex]

        track["image"] = album.image
        upsert_id = instances.tracks_instance.insert_song(track)

        track["_id"] = {"$oid": str(upsert_id)}
        api.TRACKS.append(models.Track(track))

        _bar.next()

    _bar.finish()

    Log(f"Added {len(tagged_tracks)} new tracks and {len(albums)} new albums")

    _bar = Bar("Creating folders", max=len(folders))
    for folder in folders:
        if folder not in api.VALID_FOLDERS:
            api.VALID_FOLDERS.add(folder)
            fff = folderslib.create_folder(folder)
            api.FOLDERS.add(fff)

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
