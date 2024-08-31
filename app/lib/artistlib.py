import os
import time
import urllib
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, PngImagePlugin, UnidentifiedImageError
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import ReadTimeout

from app import settings
from app.models.artist import Artist
from app.store.artists import ArtistStore

# from app.db.libdata import ArtistTable

# from app.store import artists as artist_store
# from app.store.tracks import TrackStore
from app.utils.hashing import create_hash
from app.utils.progressbar import tqdm

CHECK_ARTIST_IMAGES_KEY = ""

LARGE_ENOUGH_NUMBER = 100
PngImagePlugin.MAX_TEXT_CHUNK = LARGE_ENOUGH_NUMBER * (1024**2)
# https://stackoverflow.com/a/61466412

import random

def get_artist_image_link(artist: str):
    """
    Returns an artist image url.
    """
    response: requests.Response | None = None

    def make_request():
        query = urllib.parse.quote(artist)  # type: ignore
        url = f"https://api.deezer.com/search/artist?q={query}"
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.deezer.com/",
            "Origin": "https://www.deezer.com",
        }
        return requests.get(url, headers=headers, timeout=30)

    for attempt in range(5):
        try:
            response = make_request()
            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError:
                return None

            for res in data["data"]:
                res_hash = create_hash(res["name"], decode=True)
                artist_hash = create_hash(artist, decode=True)

                if res_hash == artist_hash:
                    return str(res["picture_big"])

            return None
        except (RequestConnectionError, ReadTimeout, IndexError, KeyError):
            if attempt == 4:
                print("Failed to get artist image link  ")

            if attempt <= 4:
                time.sleep(10)
            else:
                return None

        # except (IndexError, KeyError):
        #     print(f"Encountered index/key error in attempt {attempt}")
        #     if response is not None:
        #         print(response.headers)

        #     return None


# TODO: Move network calls to utils/network.py
class DownloadImage:
    def __init__(self, url: str, name: str) -> None:
        img = self.download(url)

        if img is None:
            return

        sm_path = Path(settings.Paths.get_sm_artist_img_path()) / name
        lg_path = Path(settings.Paths.get_lg_artist_img_path()) / name
        md_path = Path(settings.Paths.get_md_artist_img_path()) / name

        entries = [
            (lg_path, None),  # save in the original size
            (sm_path, settings.Defaults.SM_ARTIST_IMG_SIZE),
            (md_path, settings.Defaults.MD_ARTIST_IMG_SIZE),
        ]

        self.save_img(img, entries)

    @staticmethod
    def download(url: str) -> Image.Image | None:
        """
        Downloads the image from the url.
        Retries after 10 seconds on a connection error.
        """
        for attempt in range(2):
            try:
                response = requests.get(url, timeout=10)
                return Image.open(BytesIO(response.content))
            except (RequestConnectionError, requests.Timeout, ReadTimeout):
                if attempt == 0:
                    time.sleep(10)
                else:
                    return None
            except UnidentifiedImageError:
                return None

    @staticmethod
    def save_img(img: Image.Image, entries: list[tuple[Path, int | None]]):
        """
        Saves the image to the destinations.
        """
        ratio = img.width / img.height
        for entry in entries:
            path, size = entry

            if size is None:
                img.save(path, format="webp")
                continue

            img.resize((size, int(size / ratio)), Image.ANTIALIAS).save(
                path, format="webp"
            )


class CheckArtistImages:
    def __init__(self, instance_key: str):
        global CHECK_ARTIST_IMAGES_KEY
        CHECK_ARTIST_IMAGES_KEY = instance_key

        # read all files in the artist image folder
        path = settings.Paths.get_sm_artist_img_path()
        processed = [path.replace(".webp", "") for path in os.listdir(path)]

        unprocessed = [
            a for a in ArtistStore.get_flat_list() if a.artisthash not in processed
        ]

        key_artist_map = ((instance_key, artist) for artist in unprocessed)

        with ThreadPoolExecutor(max_workers=14) as executor:
            res = list(
                tqdm(
                    executor.map(self.download_image, key_artist_map),
                    total=len(unprocessed),
                    desc="Downloading missing artist images",
                )
            )

            list(res)

    @staticmethod
    def download_image(_map: tuple[str, Artist]):
        """
        Checks if an artist image exists and downloads it if not.

        :param artist: The artist name
        """
        instance_key, artist = _map

        if CHECK_ARTIST_IMAGES_KEY != instance_key:
            return

        img_path = (
            Path(settings.Paths.get_sm_artist_img_path()) / f"{artist.artisthash}.webp"
        )

        if img_path.exists():
            return

        url = get_artist_image_link(artist.name)

        if url is not None:
            return DownloadImage(url, name=f"{artist.artisthash}.webp")
