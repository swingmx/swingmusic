from dataclasses import asdict

from swingmusic.models.track import Track


def serialize_track(track: Track, to_remove:set=set(), remove_disc:bool=True) -> dict:
    """
    Convert `Track` to dict

    :params track: Track to convert
    :params to_remove: custom tags which should also be removed from Track.
    :params remove_disc:
    """
    album_dict = asdict(track)
    album_keys =  ( key for key in album_dict.keys() if key.startswith(("is_", "_")) )
    # add all keys from album_dict starting with "is_" or "_"

    props = {
        "date",
        "genre",
        "last_mod",
        "og_title",
        "og_album",
        "copyright",
        "config",
        "artist_hashes",
        "created_date",
        "fav_userids",
        "playcount",
        "genrehashes",
        "id",
        "lastplayed",
        "playduration",
        "genres",
        *to_remove,
        *album_keys,
    }

    if remove_disc:
        props.add("disc")
        props.add("track")


    for key in props:
        album_dict.pop(key, None)

    # remove images
    for key in ["artists", "albumartists"]:
        for artist in album_dict[key]:
            artist.pop("image", None)

    # is_favorite @property is not included in `asdict`
    album_dict["is_favorite"] = track.is_favorite

    return album_dict


def serialize_tracks(tracks: list[Track], _remove: set = set(), remove_disc=True) -> list[dict]:
    """
    wrapper for iterable type with Tracks.
    convert Tracks to dict and return as list[dict]
    """

    return [serialize_track(t, _remove, remove_disc) for t in tracks]
