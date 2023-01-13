class AlbumMethods:
    """
    Lists all the methods that can be found in the Albums class.
    """

    def insert_album():
        """
        Inserts a new album object into the database.
        """
        pass

    def get_all_albums():
        """
        Returns all the albums in the database.
        """
        pass

    def get_album_by_id():
        """
        Returns a single album matching the passed id.
        """
        pass

    def get_album_by_name():
        """
        Returns a single album matching the passed name.
        """
        pass

    def get_album_by_artist():
        """
        Returns a single album matching the passed artist name.
        """
        pass


class ArtistMethods:
    """
    Lists all the methods that can be found in the Artists class.
    """

    def insert_artist():
        """
        Inserts a new artist object into the database.
        """
        pass

    def get_all_artists():
        """
        Returns all the artists in the database.
        """
        pass

    def get_artist_by_id():
        """
        Returns an artist matching the mongo Id.
        """
        pass

    def get_artists_by_name():
        """
        Returns all the artists matching the query.
        """
        pass


class PlaylistMethods:
    """
    Lists all the methods that can be found in the Playlists class.
    """

    def insert_playlist():
        """
        Inserts a new playlist object into the database.
        """
        pass

    def get_all_playlists():
        """
        Returns all the playlists in the database.
        """
        pass

    def get_playlist_by_id():
        """
        Returns a single playlist matching the id in the query params.
        """
        pass

    def add_track_to_playlist():
        """
        Adds a track to a playlist.
        """
        pass

    def get_playlist_by_name():
        """
        Returns a single playlist matching the name in the query params.
        """
        pass

    def update_playlist():
        """
        Updates a playlist.
        """
        pass


class TrackMethods:
    """
    Lists all the methods that can be found in the Tracks class.
    """

    def insert_one_track():
        """
        Inserts a new track object into the database.
        """
        pass

    def drop_db():
        """
        Drops the entire database.
        """
        pass

    def get_all_tracks():
        """
        Returns all the tracks in the database.
        """
        pass

    def get_track_by_id():
        """
        Returns a single track matching the id in the query params.
        """
        pass

    def get_track_by_album():
        """
        Returns a single track matching the album in the query params.
        """
        pass

    def search_tracks_by_album():
        """
        Returns all the tracks matching the albums in the query params (using regex).
        """
        pass

    def search_tracks_by_artist():
        """
        Returns all the tracks matching the artists in the query params.
        """
        pass

    def find_track_by_title():
        """
        Finds all the tracks matching the title in the query params.
        """
        pass

    def find_tracks_by_album():
        """
        Finds all the tracks matching the album in the query params.
        """
        pass

    def find_tracks_by_folder():
        """
        Finds all the tracks matching the folder in the query params.
        """
        pass

    def find_tracks_by_artist():
        """
        Finds all the tracks matching the artist in the query params.
        """
        pass

    def find_tracks_by_albumartist():
        """
        Finds all the tracks matching the album artist in the query params.
        """
        pass

    def get_track_by_path():
        """
        Returns a single track matching the path in the query params.
        """
        pass

    def remove_track_by_path():
        """
        Removes a track from the database. Returns a boolean indicating success or failure of the operation.
        """
        pass

    def remove_track_by_id():
        """
        Removes a track from the database. Returns a boolean indicating success or failure of the operation.
        """
        pass

    def find_tracks_by_albumhash():
        """
        Returns all the tracks matching the passed hash.
        """
        pass

    def get_dir_t_count():
        """
        Returns a list of all the tracks matching the path in the query params.
        """
        pass
