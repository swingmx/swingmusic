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
from app.models import Album, Artist

from app.store.artists import ArtistStore
from app.store.albums import AlbumStore


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
        albums = [a for a in AlbumStore.albums if len(a.colors) == 0]

        with SQLiteManager() as cur:
            for album in tqdm(albums, desc="Processing missing album colors"):
                colors = self.process_color(album)

                if colors is None:
                    continue

                album.set_colors(colors)

                color_str = json.dumps(colors)
                db.insert_one_album(cur, album.albumhash, color_str)

    @staticmethod
    def process_color(album: Album):
        path = Path(settings.Paths.SM_THUMB_PATH) / album.image

        if not path.exists():
            return

        colors = get_image_colors(str(path))
        return colors


class ProcessArtistColors:
    """
    Extracts the most dominant color from the artist art and saves it to the database.
    """

    def __init__(self) -> None:
        all_artists = [a for a in ArtistStore.artists if len(a.colors) == 0]

        for artist in tqdm(all_artists, desc="Processing missing artist colors"):
            self.process_color(artist)

    @staticmethod
    def process_color(artist: Artist):
        path = Path(settings.Paths.ARTIST_IMG_SM_PATH) / artist.image

        if not path.exists():
            return

        colors = get_image_colors(str(path))

        if len(colors) > 0:
            adb.insert_one_artist(artisthash=artist.artisthash, colors=colors)
            ArtistStore.map_artist_color((0, artist.artisthash, json.dumps(colors)))

# TODO: If item color is in db, get it, assign it to the item and continue.
#   - Format all colors in the format: rgb(123, 123, 123)
#   - Each digit should be 3 digits long.
#   - Format all db colors into a master string of the format "-itemhash:colorhash-"
#   - Find the item hash using index() and get the color using the index + number, where number
#       is the length of the rgb string + 1
#   - Assign the color to the item and continue.
#   - If the color is not in the db, extract it and add it to the db.
