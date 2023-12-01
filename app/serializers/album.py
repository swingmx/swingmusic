from dataclasses import asdict
from app.models import Album


def album_serializer(album: Album, to_remove: set[str]) -> dict:
    try:
        album_dict = asdict(album)
    except TypeError:
        return {}

    to_remove.update(key for key in album_dict.keys() if key.startswith("is_"))
    for key in to_remove:
        album_dict.pop(key, None)

    # remove artist images
    for artist in album_dict["albumartists"]:
        artist.pop("image", None)

    return album_dict


def serialize_for_card(album: Album):
    props_to_remove = {
        "duration",
        "count",
        "albumartists_hashes",
        "og_title",
        "base_title",
        "genres",
    }

    return album_serializer(album, props_to_remove)


def serialize_for_card_many(albums: list[Album]):
    return [serialize_for_card(a) for a in albums]
