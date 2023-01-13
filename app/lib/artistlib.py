import urllib
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from requests.exceptions import ConnectionError as ReqConnError
from requests.exceptions import ReadTimeout
from tqdm import tqdm

from app import settings
from app.db.store import Store
from app.models import Artist
from app.utils import create_hash


def get_artist_image_link(artist: str):
    """
    Returns an artist image url.
    """

    try:
        query = urllib.parse.quote(artist)  # type: ignore

        url = f"https://api.deezer.com/search/artist?q={query}"
        response = requests.get(url, timeout=30)
        data = response.json()

        for res in data["data"]:
            res_hash = create_hash(res["name"], decode=True)
            artist_hash = create_hash(artist, decode=True)

            if res_hash == artist_hash:
                return res["picture_big"]

        return None
    except (ReqConnError, ReadTimeout, IndexError, KeyError):
        return None


class DownloadImage:
    def __init__(self, url: str, name: str) -> None:
        sm_path = Path(settings.ARTIST_IMG_SM_PATH) / name
        lg_path = Path(settings.ARTIST_IMG_LG_PATH) / name

        img = self.download(url)

        if img is not None:
            self.save_img(img, sm_path, lg_path)

    @staticmethod
    def download(url: str) -> Image.Image | None:
        """
        Downloads the image from the url.
        """
        return Image.open(BytesIO(requests.get(url, timeout=10).content))

    @staticmethod
    def save_img(img: Image.Image, sm_path: Path, lg_path: Path):
        """
        Saves the image to the destinations.
        """
        img.save(lg_path, format="webp")

        sm_size = settings.SM_ARTIST_IMG_SIZE
        img.resize((sm_size, sm_size), Image.ANTIALIAS).save(sm_path, format="webp")


class CheckArtistImages:
    def __init__(self):
        with ThreadPoolExecutor() as pool:
            list(
                tqdm(
                    pool.map(self.download_image, Store.artists),
                    total=len(Store.artists),
                    desc="Downloading artist images",
                )
            )

    @staticmethod
    def download_image(artist: Artist):
        """
        Checks if an artist image exists and downloads it if not.

        :param artistname: The artist name
        """
        img_path = Path(settings.ARTIST_IMG_SM_PATH) / f"{artist.artisthash}.webp"

        if img_path.exists():
            return

        url = get_artist_image_link(artist.name)

        if url is not None:
            return DownloadImage(url, name=f"{artist.artisthash}.webp")


# def fetch_album_bio(title: str, albumartist: str) -> str | None:
#     """
#     Returns the album bio for a given album.
#     """
#     last_fm_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json".format(
#         settings.LAST_FM_API_KEY, albumartist, title
#     )

#     try:
#         response = requests.get(last_fm_url)
#         data = response.json()
#     except:
#         return None

#     try:
#         bio = data["album"]["wiki"]["summary"].split('<a href="https://www.last.fm/')[0]
#     except KeyError:
#         bio = None

#     return bio


# class FetchAlbumBio:
#     """
#     Returns the album bio for a given album.
#     """

#     def __init__(self, title: str, albumartist: str):
#         self.title = title
#         self.albumartist = albumartist

#     def __call__(self):
#         return fetch_album_bio(self.title, self.albumartist)
