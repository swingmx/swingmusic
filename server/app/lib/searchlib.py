"""
This library contains all the functions related to the search functionality.
"""
from typing import List

from app import api
from app import helpers
from app import models
from app.lib import albumslib
from rapidfuzz import fuzz
from rapidfuzz import process

ratio = fuzz.ratio
wratio = fuzz.WRatio


class Cutoff:
    """
    Holds all the default cutoff values.
    """

    tracks: int = 70
    albums: int = 70
    artists: int = 70


class Limit:
    """
    Holds all the default limit values.
    """

    tracks: int = 50
    albums: int = 50
    artists: int = 50


class SearchTracks:

    def __init__(self, query) -> None:
        self.query = query

    def __call__(self) -> List[models.Track]:
        """
        Gets all songs with a given title.
        """

        tracks = [track.title for track in api.TRACKS]
        results = process.extract(
            self.query,
            tracks,
            scorer=fuzz.WRatio,
            score_cutoff=Cutoff.tracks,
            limit=Limit.tracks,
        )

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

        f_artists = set()

        for artist in artists:
            for a in artist:
                f_artists.add(a)

        return f_artists

    def __call__(self) -> list:
        """
        Gets all artists with a given name.
        """

        artists = self.get_all_artist_names()
        results = process.extract(
            self.query,
            artists,
            scorer=fuzz.WRatio,
            score_cutoff=Cutoff.artists,
            limit=Limit.artists,
        )

        f_artists = []
        for artist in results:
            aa = {
                "name": artist[0],
                "image": helpers.create_safe_name(artist[0]) + ".webp",
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

        albums = [a.title for a in api.ALBUMS]
        results = process.extract(
            self.query,
            albums,
            scorer=fuzz.WRatio,
            score_cutoff=Cutoff.albums,
            limit=Limit.albums,
        )

        return [api.ALBUMS[i[2]] for i in results]

        # get all artists that matched the query
        # for get all albums from the artists
        # get all albums that matched the query
        # return [**artist_albums **albums]

        # recheck next and previous artist on play next or add to playlist


class GetTopArtistTracks:

    def __init__(self, artist: str) -> None:
        self.artist = artist

    def __call__(self) -> List[models.Track]:
        """
        Gets all tracks from a given artist.
        """

        return [track for track in api.TRACKS if self.artist in track.artists]


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
        track for track in api.TRACKS
        if artist.lower() in str(track.artists).lower()
    ]
