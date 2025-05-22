"""
Contains everything that deals with image color extraction.
"""

from pathlib import Path

import colorgram

from swingmusic import settings

from swingmusic.db.userdata import LibDataTable
from swingmusic.logger import log
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.utils.progressbar import tqdm

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
        else settings.Paths.get_sm_artist_img_path()
    )
    path = Path(path) / (item_hash + ".webp")

    if not path.exists():
        return

    return get_image_colors(str(path))


class ProcessAlbumColors:
    """
    Extracts the most dominant color from the album art and saves it to the database.
    """

    def __init__(self) -> None:
        albums = [a for a in AlbumStore.get_flat_list() if not a.color]

        for album in tqdm(albums, desc="Processing missing album colors"):
            albumhash = album.albumhash

            albumrecord = LibDataTable.find_one(albumhash, type="album")
            if albumrecord is not None and albumrecord.color is not None:
                continue

            colors = process_color(albumhash)

            if colors is None:
                continue

            album = AlbumStore.albummap.get(albumhash)

            if album:
                album.set_color(colors[0])

            # INFO: Write to the database.
            if albumrecord is None:
                LibDataTable.insert_one(
                    {
                        "itemhash": "album" + albumhash,
                        "color": colors[0],
                        "itemtype": "album",
                    }
                )
            else:
                LibDataTable.update_one(albumhash, {"color": colors[0]})


class ProcessArtistColors:
    """
    Extracts the most dominant color from the artist art and saves it to the database.
    """

    def __init__(self) -> None:
        all_artists = [a for a in ArtistStore.get_flat_list() if not a.color]

        for artist in tqdm(all_artists, desc="Processing missing artist colors"):
            artisthash = artist.artisthash

            record = LibDataTable.find_one(artisthash, "artist")
            if (record is not None) and (record.color is not None):
                continue

            colors = process_color(artisthash, is_album=False)

            if colors is None:
                continue

            artist = ArtistStore.artistmap.get(artisthash)

            if artist:
                artist.set_color(colors[0])

            if record is None:
                LibDataTable.insert_one(
                    {
                        "itemhash": "artist" + artisthash,
                        "color": colors[0],
                        "itemtype": "artist",
                    }
                )
            else:
                LibDataTable.update_one("artist" + artisthash, {"color": colors[0]})
