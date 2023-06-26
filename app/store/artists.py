import json

from tqdm import tqdm

from app.db.sqlite.artists import SQLiteArtistMethods as ardb
from app.lib.artistlib import get_all_artists
from app.models import Artist
from app.utils.bisection import UseBisection
from .tracks import TrackStore
from .albums import AlbumStore


class ArtistStore:
    artists: list[Artist] = []

    @classmethod
    def load_artists(cls):
        """
        Loads all artists from the database into the store.
        """
        cls.artists = get_all_artists(TrackStore.tracks, AlbumStore.albums)

        # db_artists: list[tuple] = list(ardb.get_all_artists())

        for art in tqdm(ardb.get_all_artists(), desc="Loading artists"):
            cls.map_artist_color(art)

    @classmethod
    def map_artist_color(cls, artist_tuple: tuple):
        """
        Maps a color to the corresponding artist.
        """

        artisthash = artist_tuple[1]
        color = json.loads(artist_tuple[2])

        for artist in cls.artists:
            if artist.artisthash == artisthash:
                artist.set_colors(color)
                break

    @classmethod
    def add_artist(cls, artist: Artist):
        """
        Adds an artist to the store.
        """
        cls.artists.append(artist)

    @classmethod
    def add_artists(cls, artists: list[Artist]):
        """
        Adds multiple artists to the store.
        """
        for artist in artists:
            if artist not in cls.artists:
                cls.artists.append(artist)

    @classmethod
    def get_artist_by_hash(cls, artisthash: str) -> Artist:
        """
        Returns an artist by its hash.P
        """
        artists = sorted(cls.artists, key=lambda x: x.artisthash)
        try:
            artist = UseBisection(artists, "artisthash", [artisthash])()[0]
            return artist
        except IndexError:
            return None

    @classmethod
    def get_artists_by_hashes(cls, artisthashes: list[str]) -> list[Artist]:
        """
        Returns artists by their hashes.
        """
        artists = sorted(cls.artists, key=lambda x: x.artisthash)
        artists = UseBisection(artists, "artisthash", artisthashes)()
        return [a for a in artists if a is not None]

    @classmethod
    def artist_exists(cls, artisthash: str) -> bool:
        """
        Checks if an artist exists.
        """
        return artisthash in "-".join([a.artisthash for a in cls.artists])

    @classmethod
    def artist_has_tracks(cls, artisthash: str) -> bool:
        """
        Checks if an artist has tracks.
        """
        artists: set[str] = set()

        for track in TrackStore.tracks:
            artists.update(track.artist_hashes)
            album_artists: list[str] = [a.artisthash for a in track.albumartist]
            artists.update(album_artists)

        master_hash = "-".join(artists)
        return artisthash in master_hash

    @classmethod
    def remove_artist_by_hash(cls, artisthash: str):
        """
        Removes an artist from the store.
        """
        cls.artists = [a for a in cls.artists if a.artisthash != artisthash]
