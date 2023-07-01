from dataclasses import asdict
from app.models.album import Album


def album_serializer(album: Album, to_remove: set[str]) -> dict:
    album_dict = asdict(album)

    to_remove.update(key for key in album_dict.keys() if key.startswith("is_"))
    for key in to_remove:
        album_dict.pop(key, None)

    return album_dict


def serialize_for_card(album: Album):
    props_to_remove = {
        "duration",
        "count",
        "albumartist_hashes",
        "og_title",
        "base_title",
        "genres",
    }

    return album_serializer(album, props_to_remove)


def serialize_for_card_many(albums: list[Album]):
    return [serialize_for_card(a) for a in albums]
