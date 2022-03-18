import os
from trace import Trace
from typing import List
from app import models, instances
from app import albumslib, api
from app.helpers import remove_duplicates

def create_all_tracks() -> List[models.Track]:
    """
    Gets all songs under the ~/ directory.
    """
    print("Getting all songs...")
    tracks: list[models.Track] = []

    for track in instances.songs_instance.get_all_songs():
        # print(track)
        # print(albumslib.ALBUMS)
        try:
            os.chmod(track["filepath"], 0o755)
        except FileNotFoundError:
            instances.songs_instance.remove_song_by_filepath(track["filepath"])

        album = albumslib.find_album(track["album"], track["albumartist"])
        # print(album)
        # print(track["album"], track["albumartist"])

        track["image"] = album.image

        tracks.append(models.Track(track))

    api.TRACKS.clear()
    api.TRACKS.extend(tracks)


def get_album_tracks(albumname, artist):
    """Returns all tracks matching an album"""
    _tracks: List[models.Track] = []

    for track in api.TRACKS:
        if track.album == albumname and track.albumartist == artist:
            _tracks.append(track)

    return remove_duplicates(_tracks)
