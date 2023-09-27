"""
Contains everything that deals with image color extraction.
"""

import json
from pathlib import Path

import colorgram

from app import settings
from app.db.sqlite.albumcolors import SQLiteAlbumMethods as aldb
from app.db.sqlite.artistcolors import SQLiteArtistMethods as adb
from app.db.sqlite.utils import SQLiteManager

from app.store.artists import ArtistStore
from app.store.albums import AlbumStore
from app.logger import log
from app.lib.errors import PopulateCancelledError
from app.utils.progressbar import tqdm

PROCESS_ALBUM_COLORS_KEY = ""
PROCESS_ARTIST_COLORS_KEY = ""


def get_image_colors(image: str, count=1) -> list[str]:
    """Extracts n number of the most dominant colors from an image."""
    try:
        colors = sorted(colorgram.extract(image, count), key=lambda c: c.hsl.h)
    except OSError:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


def process_color(item_hash: str, is_album=True):
    path = (
        settings.Paths.get_sm_thumb_path()
        if is_album
        else settings.Paths.get_artist_img_sm_path()
    )
    path = Path(path) / (item_hash + ".webp")

    if not path.exists():
        return

    return get_image_colors(str(path))


class ProcessAlbumColors:
    """
    Extracts the most dominant color from the album art and saves it to the database.
    """

    def __init__(self, instance_key: str) -> None:
        global PROCESS_ALBUM_COLORS_KEY
        PROCESS_ALBUM_COLORS_KEY = instance_key

        albums = [
            a
            for a in AlbumStore.albums
            if a is not None and a.colors is not None and len(a.colors) == 0
        ]

        with SQLiteManager() as cur:
            try:
                for album in tqdm(albums, desc="Processing missing album colors"):
                    if PROCESS_ALBUM_COLORS_KEY != instance_key:
                        raise PopulateCancelledError(
                            "A newer 'ProcessAlbumColors' instance is running. Stopping this one."
                        )

                    # TODO: Stop hitting the database for every album.
                    # Instead, fetch all the data from the database and
                    # check from memory.

                    exists = aldb.exists(album.albumhash, cur=cur)
                    if exists:
                        continue

                    colors = process_color(album.albumhash)

                    if colors is None:
                        continue

                    album.set_colors(colors)
                    color_str = json.dumps(colors)
                    aldb.insert_one_album(cur, album.albumhash, color_str)
            finally:
                cur.close()


class ProcessArtistColors:
    """
    Extracts the most dominant color from the artist art and saves it to the database.
    """

    def __init__(self, instance_key: str) -> None:
        all_artists = [a for a in ArtistStore.artists if len(a.colors) == 0]

        global PROCESS_ARTIST_COLORS_KEY
        PROCESS_ARTIST_COLORS_KEY = instance_key

        with SQLiteManager() as cur:
            try:
                for artist in tqdm(
                    all_artists, desc="Processing missing artist colors"
                ):
                    if PROCESS_ARTIST_COLORS_KEY != instance_key:
                        raise PopulateCancelledError(
                            "A newer 'ProcessArtistColors' instance is running. Stopping this one."
                        )

                    exists = adb.exists(artist.artisthash, cur=cur)

                    if exists:
                        continue

                    colors = process_color(artist.artisthash, is_album=False)

                    if colors is None:
                        continue

                    artist.set_colors(colors)
                    adb.insert_one_artist(cur, artist.artisthash, colors)
            finally:
                cur.close()
