"""
This library contains all the functions related to playlists.
"""
from progress.bar import Bar
from app import api, instances, models, exceptions, helpers

from app.lib import trackslib

TrackExistsInPlaylist = exceptions.TrackExistsInPlaylist


def add_track(playlistid: str, trackid: str):
    """
    Adds a track to a playlist in the api.PLAYLISTS dict and to the database.
    """
    for playlist in api.PLAYLISTS:
        if playlist.playlistid == playlistid:
            tt = trackslib.get_track_by_id(trackid)

            track = {
                "title": tt.title,
                "artists": tt.artists,
                "album": tt.album,
            }

            try:
                playlist.add_track(track)
                instances.playlist_instance.add_track_to_playlist(playlistid, track)
                return
            except TrackExistsInPlaylist as e:
                return {"error": str(e)}, 409


def get_playlist_tracks(pid: str):
    for p in api.PLAYLISTS:
        if p.playlistid == pid:
            return p.tracks


def create_all_playlists():
    """
    Gets all playlists from the database.
    """
    playlists = instances.playlist_instance.get_all_playlists()

    _bar = Bar("Creating playlists", max=len(playlists))
    for playlist in playlists:
        api.PLAYLISTS.append(models.Playlist(playlist))
        _bar.next()
    _bar.finish()
