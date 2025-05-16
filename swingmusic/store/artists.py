import json
from typing import Iterable

from swingmusic.lib.tagger import create_artists
from swingmusic.models import Artist
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.customlist import CustomList
from .tracks import TrackStore

ARTIST_LOAD_KEY = ""


class ArtistMapEntry:
    def __init__(
        self, artist: Artist, albumhashes: set[str], trackhashes: set[str]
    ) -> None:
        self.artist = artist
        self.albumhashes: set[str] = albumhashes
        self.trackhashes: set[str] = trackhashes

    def increment_playcount(self, duration: int, timestamp: int, playcount: int = 1):
        self.artist.lastplayed = timestamp
        self.artist.playduration += duration
        self.artist.playcount += playcount

    def toggle_favorite_user(self, userid: int | None = None):
        if userid is None:
            userid = get_current_userid()

        self.artist.toggle_favorite_user(userid)

    def set_color(self, color: str):
        self.artist.color = color


class ArtistStore:
    artistmap: dict[str, ArtistMapEntry] = {}

    @classmethod
    def load_artists(cls, instance_key: str, _trackhashes: list[str] = []):
        """
        Loads all artists from the database into the store.
        """
        global ARTIST_LOAD_KEY
        ARTIST_LOAD_KEY = instance_key

        print("Loading artists... ", end="")
        cls.artistmap.clear()

        cls.artistmap = {
            artist.artisthash: ArtistMapEntry(
                artist=artist, albumhashes=albumhashes, trackhashes=trackhashes
            )
            for artist, trackhashes, albumhashes in create_artists(_trackhashes)
        }

        # for track in TrackStore.get_flat_list():
        #     if instance_key != ARTIST_LOAD_KEY:
        #         return

        #     for hash in track.artisthashes:
        #         cls.artistmap[hash].trackhashes.add(track.trackhash)
        #         cls.artistmap[hash].albumhashes.add(track.albumhash)

        print("Done!")
        # for artist in ardb.get_all_artists():
        #     if instance_key != ARTIST_LOAD_KEY:
        #         return

        #     cls.map_artist_color(artist)

    @classmethod
    def get_flat_list(cls):
        """
        Returns a flat list of all artists.
        """
        return [a.artist for a in cls.artistmap.values()]

    # @classmethod
    # def map_artist_color(cls, artist_tuple: tuple):
    #     """
    #     Maps a color to the corresponding artist.
    #     """

    #     artisthash = artist_tuple[1]
    #     color = json.loads(artist_tuple[2])

    #     for artist in cls.artists:
    #         if artist.artisthash == artisthash:
    #             artist.set_colors(color)
    #             break

    # @classmethod
    # def add_artist(cls, artist: Artist):
    #     """
    #     Adds an artist to the store.
    #     """
    #     cls.artists.append(artist)

    # @classmethod
    # def add_artists(cls, artists: list[Artist]):
    #     """
    #     Adds multiple artists to the store.
    #     """
    #     for artist in artists:
    #         if artist not in cls.artists:
    #             cls.artists.append(artist)

    @classmethod
    def get_artist_by_hash(cls, artisthash: str):
        """
        Returns an artist by its hash.P
        """
        entry = cls.artistmap.get(artisthash, None)
        if entry is not None:
            return entry.artist

    @classmethod
    def get_artists_by_hashes(cls, artisthashes: Iterable[str]):
        """
        Returns artists by their hashes.
        """
        artists = [cls.get_artist_by_hash(hash) for hash in artisthashes]
        return [a for a in artists if a is not None]

    # @classmethod
    # def artist_exists(cls, artisthash: str) -> bool:
    #     """
    #     Checks if an artist exists.
    #     """
    #     return artisthash in "-".join([a.artisthash for a in cls.artists])

    # @classmethod
    # def artist_has_tracks(cls, artisthash: str) -> bool:
    #     """
    #     Checks if an artist has tracks.
    #     """
    #     artists: set[str] = set()

    #     for track in TrackStore.tracks:
    #         artists.update(track.artist_hashes)
    #         album_artists: list[str] = [a.artisthash for a in track.albumartists]
    #         artists.update(album_artists)

    #     master_hash = "-".join(artists)
    #     return artisthash in master_hash

    # @classmethod
    # def remove_artist_by_hash(cls, artisthash: str):
    #     """
    #     Removes an artist from the store.
    #     """
    #     cls.artists = CustomList(a for a in cls.artists if a.artisthash != artisthash)

    @classmethod
    def get_artist_tracks(cls, artisthash: str):
        """
        Returns all tracks by the given artist hash.
        """
        entry = cls.artistmap.get(artisthash)
        if entry is not None:
            return TrackStore.get_tracks_by_trackhashes(entry.trackhashes)

        return []

    @classmethod
    def export(cls):
        path = "artists.json"

        with open(path, "w") as f:
            data = [
                {
                    "name": a.name,
                }
                for a in cls.get_flat_list()
            ]
            json.dump(data, f)
