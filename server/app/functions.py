"""
This module contains functions for the server
"""
import os
import time
from io import BytesIO

import requests
from app import api
from app import helpers
from app import settings
from app.lib import watchdoge
from app.lib.populate import Populate
from PIL import Image
from progress.bar import Bar

from app.lib.trackslib import create_all_tracks


@helpers.background
def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """
    is_underway = False

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
    pop = Populate()
    pop.run()

    tracks = create_all_tracks()
    api.TRACKS.clear()
    api.TRACKS.extend(tracks)


@helpers.background
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


@helpers.background
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


# TODO
# - Move the populate function to a new file and probably into a new class
# - Start movement from functional programming to OOP to OOP
