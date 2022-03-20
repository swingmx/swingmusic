from app import api, instances, models
from app.lib import trackslib


def add_track(playlistid: str, trackid: str):
    """
    Adds a track to a playlist in the api.PLAYLISTS dict and to the database.
    """
    for playlist in api.PLAYLISTS:
        if playlist.playlistid == playlistid:
            track = trackslib.get_track_by_id(trackid)
            playlist.tracks.append(track)

            instances.playlist_instance.add_track_to_playlist(playlistid, track)




def create_all_playlists():
    """
    Gets all playlists from the database.
    """
    for playlist in instances.playlist_instance.get_all_playlists():
        api.PLAYLISTS.append(models.Playlist(playlist))
