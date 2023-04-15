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

from app.store.artists import ArtistStore
from app.store.albums import AlbumStore


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
    path = settings.Paths.get_sm_thumb_path() if is_album else settings.Paths.get_artist_img_sm_path()
    path = Path(path) / (item_hash + ".webp")

    if not path.exists():
        return

    return get_image_colors(str(path))


class ProcessAlbumColors:
    """
    Extracts the most dominant color from the album art and saves it to the database.
    """

    def __init__(self) -> None:
        albums = [a for a in AlbumStore.albums if len(a.colors) == 0]

        with SQLiteManager() as cur:
            for album in tqdm(albums, desc="Processing missing album colors"):
                sql = "SELECT COUNT(1) FROM albums WHERE albumhash = ?"
                cur.execute(sql, (album.albumhash,))
                count = cur.fetchone()[0]

                if count != 0:
                    continue

                colors = process_color(album.albumhash)

                if colors is None:
                    continue

                album.set_colors(colors)
                color_str = json.dumps(colors)
                db.insert_one_album(cur, album.albumhash, color_str)


class ProcessArtistColors:
    """
    Extracts the most dominant color from the artist art and saves it to the database.
    """

    def __init__(self) -> None:
        all_artists = [a for a in ArtistStore.artists if len(a.colors) == 0]

        with SQLiteManager() as cur:
            for artist in tqdm(all_artists, desc="Processing missing artist colors"):
                sql = "SELECT COUNT(1) FROM artists WHERE artisthash = ?"

                cur.execute(sql, (artist.artisthash,))
                count = cur.fetchone()[0]

                if count != 0:
                    continue

                colors = process_color(artist.artisthash, is_album=False)

                if colors is None:
                    continue

                artist.set_colors(colors)
                adb.insert_one_artist(cur, artist.artisthash, colors)
