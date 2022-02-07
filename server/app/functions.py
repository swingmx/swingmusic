"""
This module contains larger functions for the server
"""

import time
import os
from io import BytesIO
import random
import datetime
import mutagen

import requests
from mutagen.flac import MutagenError
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from progress.bar import Bar
from PIL import Image

from app import helpers
from app import instances
from app import api
from app import models


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

    api.all_the_f_music = helpers.get_all_songs()
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


def extract_thumb(audio_file_path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """

    album_art = None

    webp_path = audio_file_path.split("/")[-1] + ".webp"
    img_path = os.path.join(helpers.app_dir, "images", "thumbnails", webp_path)

    if os.path.exists(img_path):
        return webp_path

    if audio_file_path.endswith(".flac"):
        try:
            audio = FLAC(audio_file_path)
            album_art = audio.pictures[0].data
        except:
            album_art = None
    elif audio_file_path.endswith(".mp3"):
        try:
            audio = ID3(audio_file_path)
            album_art = audio.getall("APIC")[0].data
        except:
            album_art = None

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
                return use_defaults()

        return webp_path
    else:
        return use_defaults()


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


def get_tags(full_path: str) -> dict:
    """
    Returns a dictionary of tags for a given file.
    """
    try:
        audio = mutagen.File(full_path, easy=True)
    except MutagenError:
        return None

    tags = {
        "artists": parse_artist_tag(audio),
        "title": parse_title_tag(audio, full_path),
        "albumartist": parse_album_artist_tag(audio),
        "album": parse_album_tag(audio),
        "genre": parse_genre_tag(audio),
        "date": parse_date_tag(audio)[:4],
        "tracknumber": parse_track_number(audio),
        "discnumber": parse_disk_number(audio),
        "length": round(audio.info.length),
        "bitrate": round(int(audio.info.bitrate) / 1000),
        "filepath": full_path.replace(helpers.home_dir, ""),
        "image": extract_thumb(full_path),
        "folder": os.path.dirname(full_path).replace(helpers.home_dir, ""),
    }

    return tags


def get_album_bio(title: str, albumartist: str):
    """
    Returns the album bio for a given album.
    """
    last_fm_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(
        helpers.LAST_FM_API_KEY, albumartist, title
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


def create_track_class(tags):
    """
    Creates a Track class from a dictionary of tags.
    """
    return models.Track(
        tags["_id"]["$oid"],
        tags["title"],
        tags["artists"],
        tags["albumartist"],
        tags["album"],
        tags["filepath"],
        tags["folder"],
        tags["length"],
        tags["date"],
        tags["genre"],
        tags["bitrate"],
        tags["image"],
        tags["tracknumber"],
        tags["discnumber"],
    )
