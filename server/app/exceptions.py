class TrackExistsInPlaylistError(Exception):
    """
    Exception raised when a track is already in a playlist.
    """

    pass


class PlaylistExistsError(Exception):
    """
    Exception raised when a playlist already exists.
    """

    pass
