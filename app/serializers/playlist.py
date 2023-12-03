from dataclasses import asdict
from app.models.playlist import Playlist


def serialize_for_card(playlist: Playlist, to_remove=set()):
    p_dict = asdict(playlist)

    props = {"trackhashes"}.union(to_remove)

    for key in props:
        p_dict.pop(key, None)

    return p_dict
