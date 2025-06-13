from dataclasses import asdict

from swingmusic.models.track import Track


def serialize_track(track: Track, to_remove: set = set(), remove_disc=True) -> dict:
    album_dict = asdict(track)
    # is_favorite @property is not included in asdict
    album_dict["is_favorite"] = track.is_favorite

    props = {
        "date",
        "genre",
        "last_mod",
        "og_title",
        "og_album",
        "copyright",
        "config",
        "disc",
        "track",
        "artist_hashes",
        "created_date",
        "fav_userids",
        "playcount",
        "genrehashes",
        "id",
        "lastplayed",
        "playduration",
        "genres",
    }.union(to_remove)

    if not remove_disc:
        props.remove("disc")
        props.remove("track")

    props.update(key for key in album_dict.keys() if key.startswith(("is_", "_")))
    props.remove("is_favorite")

    for key in props:
        album_dict.pop(key, None)

    to_remove_images = ["artists", "albumartists"]
    for key in to_remove_images:
        for artist in album_dict[key]:
            artist.pop("image", None)

    return album_dict


def serialize_tracks(
    tracks: list[Track], _remove: set = set(), remove_disc=True
) -> list[dict]:
    return [serialize_track(t, _remove, remove_disc) for t in tracks]
