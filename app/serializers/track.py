from dataclasses import asdict
from app.models.track import Track


def track_serializer(track: Track, _remove: set = {}, retain_disc=False) -> dict:
    album_dict = asdict(track)
    to_remove = {
        "date",
        "genre",
        "last_mod",
        "og_title",
        "og_album",
    }.union(_remove)

    if not retain_disc:
        to_remove.union("disc", "track")

    to_remove.update(key for key in album_dict.keys() if key.startswith("is_"))
    to_remove.remove('is_favorite')

    for key in to_remove:
        album_dict.pop(key, None)

    return album_dict


def serialize_tracks(
    tracks: list[Track], _remove: set = {}, retain_disc=False
) -> list[dict]:
    return [track_serializer(t, _remove, retain_disc) for t in tracks]
