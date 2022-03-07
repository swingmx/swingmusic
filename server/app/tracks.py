import os
from typing import List
from app import models, instances


ALL_MUSIC: List[models.Track] = []


def create_all_tracks() -> List[models.Track]:
    """
    Gets all songs under the ~/ directory.
    """
    print("Getting all songs...")

    tracks: list[models.Track] = []

    for track in instances.songs_instance.get_all_songs():
        print(track)
        try:
            os.chmod(track["filepath"], 0o755)
        except FileNotFoundError:
            instances.songs_instance.remove_song_by_filepath(track["filepath"])

        album = instances.album_instance.get_album_by_name(
            track["album"], track["albumartist"]
        )

        track["albumid"] = album["_id"]["$oid"]
        track["image"] = album["image"]

        tracks.append(models.Track(track))

    ALL_MUSIC.clear()
    ALL_MUSIC.extend(tracks)
