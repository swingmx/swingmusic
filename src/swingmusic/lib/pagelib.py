import json
from typing import Any
from swingmusic.serializers.album import serialize_for_card
from swingmusic.serializers.artist import serialize_for_card as serialize_artist
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.utils.hashing import create_hash


def validate_page_items(items: list[dict[str, str]], existing: list[dict[str, str]]):
    """
    Validate the items in a page before adding them to the database.
    """
    validated: list[dict[str, str]] = []
    indexed = set(create_hash(json.dumps(item)) for item in existing)

    for item in items:
        if create_hash(json.dumps(item)) in indexed:
            continue

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


def remove_page_items(existing: list[dict[str, str]], item: dict[str, str]):
    return [
        i
        for i in existing
        if create_hash(json.dumps(i)) != create_hash(json.dumps(item))
    ]


def recover_page_items(items: list[dict[str, str]], for_homepage: bool = False):
    """
    Recover the items in a page.
    """
    recovered: list[dict[str, Any]] = []

    for item in items:
        if item["type"] == "album":
            album = AlbumStore.albummap.get(item["hash"])

            if album is not None:
                item = serialize_for_card(album.album)

                if for_homepage:
                    del item["type"]
                    item = {"item": item, "type": "album"}

                recovered.append(item)
        elif item["type"] == "artist":
            artist = ArtistStore.artistmap.get(item["hash"])

            if artist is not None:
                item = serialize_artist(artist.artist)

                if for_homepage:
                    del item["type"]
                    item = {"item": item, "type": "artist"}

                recovered.append(item)

    recovered.reverse()
    return recovered
