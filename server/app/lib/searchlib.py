"""
This library contains all the functions related to the search functionality.
"""

from typing import List

from app import api, helpers, models
from app.lib import albumslib
from rapidfuzz import fuzz, process


class SearchTracks:
    def __init__(self, query) -> None:
        self.query = query

    def __call__(self) -> List[models.Track]:
        """
        Gets all songs with a given title.
        """

        tracks = [track.title for track in api.TRACKS]
        results = process.extract(
            self.query, tracks, scorer=fuzz.token_set_ratio, score_cutoff=50
        )
        print(results)
        return [api.TRACKS[i[2]] for i in results]


class SearchArtists:
    def __init__(self, query) -> None:
        self.query = query

    @staticmethod
    def get_all_artist_names() -> List[str]:
        """
        Gets all artist names.
        """

        artists = [track.artists for track in api.TRACKS]

        f_artists = []
        for artist in artists:
            aa = artist.split(",")
            f_artists.extend(aa)

        return f_artists

    @staticmethod
    def get_valid_name(name: str) -> str:
        """
        returns a valid artist name
        """

        return "".join([i for i in name if i not in '/\\:*?"<>|'])

    def __call__(self) -> list:
        """
        Gets all artists with a given name.
        """

        artists = self.get_all_artist_names()
        results = process.extract(self.query, artists)

        f_artists = []
        for artist in results:
            aa = {
                "name": artist[0],
                "image": self.get_valid_name(artist[0]) + ".webp",
            }
            f_artists.append(aa)

        return f_artists


class SearchAlbums:
    def __init__(self, query) -> None:
        self.query = query

    def get_albums_by_name(self) -> List[models.Album]:
        """
        Gets all albums with a given title.
        """

        albums = [album.title for album in api.ALBUMS]
        results = process.extract(self.query, albums)
        return [api.ALBUMS[i[2]] for i in results]

    def __call__(self) -> List[models.Album]:
        """
        Gets all albums with a given title.
        """

        artists = SearchArtists(self.query)()
        a_albums = []

        # get all artists that matched the query
        # for get all albums from the artists
        # get all albums that matched the query
        # return [**artist_albums **albums]


def get_search_albums(query: str) -> List[models.Album]:
    """
    Gets all songs with a given album.
    """
    return albumslib.search_albums_by_name(query)


def get_artists(artist: str) -> List[models.Track]:
    """
    Gets all songs with a given artist.
    """
    return [
        track for track in api.TRACKS if artist.lower() in str(track.artists).lower()
    ]
