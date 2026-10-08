from dataclasses import asdict

from swingmusic.models.artist import Artist


def serialize_for_card(artist: Artist, include: set[str] = set()):
    try:
        artist_dict = asdict(artist)
    except TypeError:
        return {}

    # trackcount, albumcount and duration are kept: clients show them as soon as an artist is
    # opened from a card, before the artist's own page has loaded.
    props_to_remove = {
        "is_favorite",
        "playcount",
        "playduration",
        "playcount",
        "lastplayed",
        "id",
        "genres",
        "genrehashes",
        "extra",
        "created_date",
        "date",
        "fav_userids",
        "_score",
    }

    if include:
        props_to_remove = props_to_remove - include

    for key in props_to_remove:
        artist_dict.pop(key, None)

    artist_dict["type"] = "artist"
    return artist_dict


def serialize_for_cards(artists: list[Artist]):
    return [serialize_for_card(a) for a in artists]
