"""
Contains everything that deals with image color extraction.
"""
import json
from pathlib import Path

import colorgram
from tqdm import tqdm

from app import settings
from app.db.sqlite.albums import SQLiteAlbumMethods as db
from app.db.sqlite.artists import SQLiteArtistMethods as adb
from app.db.sqlite.utils import SQLiteManager
from app.db.store import Store
from app.models import Album
from app.models import Artist


def get_image_colors(image: str) -> list[str]:
    """Extracts 2 of the most dominant colors from an image."""
    try:
        colors = sorted(colorgram.extract(image, 1), key=lambda c: c.hsl.h)
    except OSError:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


class ProcessAlbumColors:
    """
    Extracts the most dominant color from the album art and saves it to the database.
    """

    def __init__(self) -> None:

        with SQLiteManager() as cur:
            for album in tqdm(Store.albums, desc="Processing album colors"):
                if len(album.colors) == 0:
                    colors = self.process_color(album)

                    if colors is None:
                        continue

                    album.set_colors(colors)

                    color_str = json.dumps(colors)
                    db.insert_one_album(cur, album.albumhash, color_str)

    @staticmethod
    def process_color(album: Album):
        path = Path(settings.SM_THUMB_PATH) / album.image

        if not path.exists():
            return

        colors = get_image_colors(str(path))
        return colors


class ProcessArtistColors:
    """
    Extracts the most dominant color from the artist art and saves it to the database.
    """

    def __init__(self) -> None:
        all_artists = Store.artists

        if all_artists is None:
            return

        for artist in tqdm(all_artists, desc="Processing artist colors"):
            if len(artist.colors) == 0:
                self.process_color(artist)

    @staticmethod
    def process_color(artist: Artist):
        path = Path(settings.ARTIST_IMG_SM_PATH) / artist.image

        if not path.exists():
            return

        colors = get_image_colors(str(path))

        if len(colors) > 0:
            adb.insert_one_artist(artisthash=artist.artisthash, colors=colors)
            Store.map_artist_color((0, artist.artisthash, json.dumps(colors)))

    # TODO: Load album and artist colors into the store.
