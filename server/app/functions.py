"""
This module contains larger functions for the server
"""

import time
import os
import requests
import random
import datetime

from mutagen.flac import MutagenError
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from progress.bar import Bar
from PIL import Image
from io import BytesIO

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
    print("\nchecking for new tracks")
    files = helpers.run_fast_scandir(helpers.home_dir, [".flac", ".mp3"])[1]

    for file in files:
        getTags(file)

    api.all_the_f_music = helpers.getAllSongs()
    print("\ncheck done")


def populate_images():
    all_songs = instances.songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
        this_artists = song["artists"].split(", ")

        for artist in this_artists:
            if artist not in artists:
                artists.append(artist)

    bar = Bar("Processing images", max=len(artists))
    for artist in artists:
        file_path = (
            helpers.app_dir + "/images/artists/" + artist.replace("/", "::") + ".webp"
        )

        if not os.path.exists(file_path):

            def try_save_image():
                url = "https://api.deezer.com/search/artist?q={}".format(artist)
                response = requests.get(url)
                data = response.json()

                try:
                    img_path = data["data"][0]["picture_medium"]
                except:
                    img_path = None

                if img_path is not None:
                    # save image as webp
                    img = Image.open(BytesIO(requests.get(img_path).content))
                    img.save(file_path, format="webp")

            try:
                try_save_image()
            except requests.exceptions.ConnectionError:
                time.sleep(5)
                try_save_image()

        bar.next()

    bar.finish()


def extract_thumb(audio_file_path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """

    album_art = None

    def use_defaults() -> str:
        """
        Returns a path to a random image in the defaults directory.
        """
        path = str(random.randint(0, 10)) + ".webp"
        return path

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


def getTags(full_path: str) -> dict:
    """
    Returns a dictionary of tags for a given file.
    """

    if full_path.endswith(".flac"):
        try:
            audio = FLAC(full_path)
        except MutagenError:
            return
    elif full_path.endswith(".mp3"):
        try:
            audio = MP3(full_path)
        except MutagenError:
            return

    try:
        artists = audio["artist"][0]
    except KeyError:
        try:
            artists = audio["TPE1"][0]
        except:
            artists = "Unknown"
    except IndexError:
        artists = "Unknown"

    try:
        album_artist = audio["albumartist"][0]
    except KeyError:
        try:
            album_artist = audio["TPE2"][0]
        except:
            album_artist = "Unknown"
    except IndexError:
        album_artist = "Unknown"

    try:
        title = audio["title"][0]
    except KeyError:
        try:
            title = audio["TIT2"][0]
        except:
            title = full_path.split("/")[-1]
    except:
        title = full_path.split("/")[-1]

    try:
        album = audio["album"][0]
    except KeyError:
        try:
            album = audio["TALB"][0]
        except:
            album = "Unknown"
    except IndexError:
        album = "Unknown"

    try:
        genre = audio["genre"][0]
    except KeyError:
        try:
            genre = audio["TCON"][0]
        except:
            genre = "Unknown"
    except IndexError:
        genre = "Unknown"

    try:
        date = audio["date"][0]
    except KeyError:
        try:
            date = audio["TDRC"][0]
        except:
            date = "Unknown"
    except IndexError:
        date = "Unknown"

    img_path = extract_thumb(full_path)

    length = str(datetime.timedelta(seconds=round(audio.info.length)))

    if length[:2] == "0:":
        length = length.replace("0:", "")

    tags = {
        "filepath": full_path.replace(helpers.home_dir, ""),
        "folder": os.path.dirname(full_path).replace(helpers.home_dir, ""),
        "title": title,
        "artists": artists,
        "album_artist": album_artist,
        "album": album,
        "genre": genre,
        "length": length,
        "bitrate": round(int(audio.info.bitrate) / 1000),
        "date": str(date)[:4],
        "image": img_path,
    }

    instances.songs_instance.insert_song(tags)
    return tags


def getAlbumBio(title: str, album_artist: str):
    last_fm_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(
        helpers.LAST_FM_API_KEY, album_artist, title
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
    return models.Track(
        tags["_id"]["$oid"],
        tags["title"],
        tags["artists"],
        tags["album_artist"],
        tags["album"],
        tags["filepath"],
        tags["folder"],
        tags["length"],
        tags["date"],
        tags["genre"],
        tags["bitrate"],
        tags["image"],
    )
