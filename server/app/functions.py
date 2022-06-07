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
from concurrent.futures import ThreadPoolExecutor

from app.lib.trackslib import create_all_tracks


@helpers.background
def reindex_tracks():
    """
    Checks for new songs every 5 minutes.
    """

    while True:
        populate()
        CheckArtistImages()()

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


class getArtistImage:
    """
    Returns an artist image url.
    """

    def __init__(self, artist: str):
        self.artist = artist

    def __call__(self):
        try:
            url = f"https://api.deezer.com/search/artist?q={self.artist}"
            response = requests.get(url)
            data = response.json()

            return data["data"][0]["picture_medium"]
        except requests.exceptions.ConnectionError:
            time.sleep(5)
            return None
        except (IndexError, KeyError):
            return None


class useImageDownloader:
    def __init__(self, url: str, dest: str) -> None:
        self.url = url
        self.dest = dest

    def __call__(self) -> None:
        try:
            img = Image.open(BytesIO(requests.get(self.url).content))
            img.save(self.dest, format="webp")
            img.close()
        except requests.exceptions.ConnectionError:
            print("🔴🔴🔴🔴🔴🔴🔴")
            time.sleep(5)


class CheckArtistImages:
    def __init__(self):
        self.artists: list[str] = []
        print("Checking for artist images")

    @staticmethod
    def check_if_exists(img_path: str):
        """
        Checks if an image exists on disk.
        """

        if os.path.exists(img_path):
            return True
        else:
            return False

    def gather_artists(self):
        """
        Loops through all the tracks and gathers all the artists.
        """

        for song in api.DB_TRACKS:
            this_artists: list = song["artists"].split(", ")

            for artist in this_artists:
                if artist not in self.artists:
                    self.artists.append(artist)

    @classmethod
    def download_image(cls, artistname: str):
        """
        Checks if an artist image exists and downloads it if not.

        :param artistname: The artist name
        """

        img_path = (
            helpers.app_dir
            + "/images/artists/"
            + artistname.replace("/", "::")
            + ".webp"
        )

        if cls.check_if_exists(img_path):
            return

        url = getArtistImage(artistname)()

        if url is None:
            return

        useImageDownloader(url, img_path)()

    def __call__(self):
        self.gather_artists()

        with ThreadPoolExecutor() as pool:
            pool.map(self.download_image, self.artists)

        print("Done fetching images")


def fetch_album_bio(title: str, albumartist: str) -> str | None:
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


class FetchAlbumBio:
    """
    Returns the album bio for a given album.
    """

    def __init__(self, title: str, albumartist: str):
        self.title = title
        self.albumartist = albumartist

    def __call__(self):
        return fetch_album_bio(self.title, self.albumartist)


# TODO
# - Move the populate function to a new file and probably into a new class
# - Start movement from functional programming to OOP to OOP
