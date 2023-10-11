from dataclasses import asdict

from app.models.artist import Artist


def serialize_for_card(artist: Artist):
    artist_dict = asdict(artist)

    props_to_remove = {
        "is_favorite",
        "trackcount",
        "duration",
        "albumcount",
    }

    for key in props_to_remove:
        artist_dict.pop(key, None)

    return artist_dict


def serialize_for_cards(artists: list[Artist]):
    return [serialize_for_card(a) for a in artists]
