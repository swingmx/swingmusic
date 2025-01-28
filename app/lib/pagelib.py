from typing import Any
from app.serializers.album import serialize_for_card
from app.serializers.artist import serialize_for_card as serialize_artist
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore


def validate_page_items(items: list[dict[str, str]]):
    """
    Validate the items in a page before adding them to the database.
    """
    validated: list[dict[str, str]] = []

    for item in items:
        if item["type"] == "album":
            album = AlbumStore.albummap.get(item["hash"])

            if album is not None:
                validated.append(item)
        elif item["type"] == "artist":
            artist = ArtistStore.artistmap.get(item["hash"])

            if artist is not None:
                validated.append(item)
        else:
            raise ValueError(f"Invalid item type: {item['type']}")

    return validated


def recover_page_items(items: list[dict[str, str]]):
    """
    Recover the items in a page.
    """
    recovered: list[dict[str, Any]] = []

    for item in items:
        if item["type"] == "album":
            album = AlbumStore.albummap.get(item["hash"])

            if album is not None:
                recovered.append(
                    {"item": serialize_for_card(album.album), "type": "album"}
                )
        elif item["type"] == "artist":
            artist = ArtistStore.artistmap.get(item["hash"])

            if artist is not None:
                recovered.append(
                    {"item": serialize_artist(artist.artist), "type": "artist"}
                )

    recovered.reverse()
    return recovered
