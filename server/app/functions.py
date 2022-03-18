"""
This module contains functions for the server
"""

import time
import os
from io import BytesIO
import random
import datetime
from typing import List
import mutagen
import urllib

import requests
from mutagen.flac import MutagenError
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from progress.bar import Bar
from PIL import Image

from app import helpers
from app import instances
from app import api, settings, watchdoge, models, trackslib
from app import albumslib


def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """
    flag = False

    while flag is False:
        populate()
        get_all_albums()
        populate_images()
        # functions.save_t_colors()

        time.sleep(300)


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
    print("\nchecking for new tracks")

    files = helpers.run_fast_scandir(helpers.home_dir, [".flac", ".mp3"])[1]

    for file in files:
        tags = get_tags(file)

        if tags is not None:
            instances.songs_instance.insert_song(tags)

    albumslib.create_everything()

    print("\n check done")
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


def populate_images():
    """populates the artists images"""

    all_songs = instances.songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
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
                img = Image.open(BytesIO(requests.get(img_path).content))
                img.save(file_path, format="webp")

        _bar.next()

    _bar.finish()


def use_defaults() -> str:
    """
    Returns a path to a random image in the defaults directory.
    """
    path = str(random.randint(0, 10)) + ".webp"
    return path


def save_track_colors(img, filepath) -> None:
    """Saves the track colors to the database"""

    track_colors = helpers.extract_colors(img)

    tc_dict = {
        "filepath": filepath,
        "colors": track_colors,
    }

    instances.track_color_instance.insert_track_color(tc_dict)


def return_album_art(filepath):
    """
    Returns the album art for a given audio file.
    """

    if filepath.endswith(".flac"):
        try:
            audio = FLAC(filepath)
            return audio.pictures[0].data
        except:
            return None
    elif filepath.endswith(".mp3"):
        try:
            audio = ID3(filepath)
            return audio.getall("APIC")[0].data
        except:
            return None


def save_t_colors():
    tracks = instances.songs_instance.get_all_songs()
    _bar = Bar("Processing image colors", max=len(tracks))

    for track in tracks:
        filepath = track["filepath"]
        album_art = return_album_art(filepath)

        if album_art is not None:
            img = Image.open(BytesIO(album_art))
            save_track_colors(img, filepath)

        _bar.next()

    _bar.finish()


def extract_thumb(audio_file_path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """
    webp_path = audio_file_path.split("/")[-1] + ".webp"
    img_path = os.path.join(helpers.app_dir, "images", "thumbnails", webp_path)

    if os.path.exists(img_path):
        return urllib.parse.quote(webp_path)

    album_art = return_album_art(audio_file_path)

    if album_art is not None:
        img = Image.open(BytesIO(album_art))

        try:
            small_img = img.resize((250, 250), Image.ANTIALIAS)
            small_img.save(img_path, format="webp")
        except OSError:
            try:
                png = img.convert("RGB")
                small_img = png.resize((250, 250), Image.ANTIALIAS)
                small_img.save(img_path, format="webp")
            except:
                return None

        return urllib.parse.quote(webp_path)
    else:
        return None


def parse_artist_tag(audio):
    """
    Parses the artist tag from an audio file.
    """
    try:
        artists = audio["artist"][0]
    except (KeyError, IndexError):
        artists = "Unknown"

    return artists


def parse_title_tag(audio, full_path: str):
    """
    Parses the title tag from an audio file.
    """
    try:
        title = audio["title"][0]
    except (KeyError, IndexError):
        title = full_path.split("/")[-1]

    return title


def parse_album_artist_tag(audio):
    """
    Parses the album artist tag from an audio file.
    """
    try:
        albumartist = audio["albumartist"][0]
    except (KeyError, IndexError):
        albumartist = "Unknown"

    return albumartist


def parse_album_tag(audio):
    """
    Parses the album tag from an audio file.
    """
    try:
        album = audio["album"][0]
    except (KeyError, IndexError):
        album = "Unknown"

    return album


def parse_genre_tag(audio):
    """
    Parses the genre tag from an audio file.
    """
    try:
        genre = audio["genre"][0]
    except (KeyError, IndexError):
        genre = "Unknown"

    return genre


def parse_date_tag(audio):
    """
    Parses the date tag from an audio file.
    """
    try:
        date = audio["date"][0]
    except (KeyError, IndexError):
        date = "Unknown"

    return date


def parse_track_number(audio):
    """
    Parses the track number from an audio file.
    """
    try:
        track_number = audio["tracknumber"][0]
    except (KeyError, IndexError):
        track_number = "Unknown"

    return track_number


def parse_disk_number(audio):
    """
    Parses the disk number from an audio file.
    """
    try:
        disk_number = audio["discnumber"][0]
    except (KeyError, IndexError):
        disk_number = "Unknown"

    return disk_number


def get_tags(fullpath: str) -> dict:
    """
    Returns a dictionary of tags for a given file.
    """
    try:
        audio = mutagen.File(fullpath, easy=True)
    except MutagenError:
        return None

    tags = {
        "artists": parse_artist_tag(audio),
        "title": parse_title_tag(audio, fullpath),
        "albumartist": parse_album_artist_tag(audio),
        "album": parse_album_tag(audio),
        "genre": parse_genre_tag(audio),
        "date": parse_date_tag(audio)[:4],
        "tracknumber": parse_track_number(audio),
        "discnumber": parse_disk_number(audio),
        "length": round(audio.info.length),
        "bitrate": round(int(audio.info.bitrate) / 1000),
        "filepath": fullpath,
        "folder": os.path.dirname(fullpath).replace(helpers.home_dir, ""),
    }

    return tags


def get_album_bio(title: str, albumartist: str):
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
        return "None"

    try:
        bio = data["album"]["wiki"]["summary"].split('<a href="https://www.last.fm/')[0]
    except KeyError:
        bio = None

    if bio is None:
        return "None"

    return bio


def get_all_albums() -> List[models.Album]:
    print("processing albums started ...")

    all_tracks = instances.songs_instance.get_all_songs()
    album_dicts = []
    albums = []

    for track in all_tracks:
        album_dict = {
            "album": track["album"],
            "artist": track["albumartist"],
        }

        if album_dict not in album_dicts:
            album_dicts.append(album_dict)

    for album in album_dicts:
        album_tracks = [
            track
            for track in all_tracks
            if track["album"] == album["album"]
            and track["albumartist"] == album["artist"]
        ]

        album["count"] = len(album_tracks)
        album["duration"] = albumslib.get_album_duration(album_tracks)
        album["date"] = album_tracks[0]["date"]
        album["artistimage"] = urllib.parse.quote_plus(
            album_tracks[0]["albumartist"] + ".webp"
        )

        album["image"] = albumslib.get_album_image(album_tracks)

        albums.append(album)

    return [models.Album(album) for album in albums]
