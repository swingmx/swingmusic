from itertools import groupby
import json
from pprint import pprint
import random
from typing import Iterable

from app.lib.tagger import create_albums
from app.models import Album, Track
from app.store.artists import ArtistStore
from app.utils import flatten
from app.utils.auth import get_current_userid
from app.utils.customlist import CustomList
from app.utils.remove_duplicates import remove_duplicates

from ..utils.hashing import create_hash
from .tracks import TrackStore
from app.utils.progressbar import tqdm

ALBUM_LOAD_KEY = ""


class AlbumMapEntry:
    def __init__(self, album: Album, trackhashes: set[str]) -> None:
        self.album = album
        self.trackhashes = trackhashes

    @property
    def basetitle(self):
        return self.album.base_title

    def increment_playcount(self, duration: int, timestamp: int, playcount: int = 1):
        self.album.lastplayed = timestamp
        self.album.playduration += duration
        self.album.playcount += playcount

    def toggle_favorite_user(self, userid: int | None = None):
        if userid is None:
            userid = get_current_userid()

        self.album.toggle_favorite_user(userid)

    def set_color(self, color: str):
        self.album.color = color


class AlbumStore:
    # albums: list[Album] = CustomList()
    albummap: dict[str, AlbumMapEntry] = {}

    # @staticmethod
    # def create_album(track: Track):
    #     """
    #     Creates album object from a track
    #     """
    #     return Album(
    #         albumhash=track.albumhash,
    #         albumartists=track.albumartists,  # type: ignore
    #         title=track.og_album,
    #     )

    @classmethod
    def load_albums(cls, instance_key: str):
        """
        Loads all albums from the database into the store.
        """
        global ALBUM_LOAD_KEY
        ALBUM_LOAD_KEY = instance_key

        print("Loading albums... ", end="")

        cls.albummap = {
            album.albumhash: AlbumMapEntry(album=album, trackhashes=trackhashes)
            for album, trackhashes in create_albums()
        }
        print("Done!")

    @classmethod
    def index_new_album(cls, album: Album, trackhashes: set[str]):
        cls.albummap[album.albumhash] = AlbumMapEntry(
            album=album, trackhashes=trackhashes
        )

    @classmethod
    def get_flat_list(cls):
        """
        Returns a flat list of all albums.
        """
        return [a.album for a in cls.albummap.values()]

    @classmethod
    def add_album(cls, album: Album):
        """
        Adds an album to the store.
        """
        cls.albums.append(album)

    @classmethod
    def add_albums(cls, albums: list[Album]):
        """
        Adds multiple albums to the store.
        """
        cls.albums.extend(albums)

    @classmethod
    def get_albums_by_albumartist(
        cls, artisthash: str, limit: int, exclude: str
    ) -> list[Album]:
        """
        Returns N albums by the given albumartist, excluding the specified album.
        """

        albums = [album for album in cls.albums if artisthash in album.artisthashes]

        albums = [
            album
            for album in albums
            if create_hash(album.base_title) != create_hash(exclude)
        ]

        if len(albums) > limit:
            random.shuffle(albums)

        # TODO: Merge this with `cls.get_albums_by_artisthash()`
        return albums[:limit]

    @classmethod
    def get_album_by_hash(cls, albumhash: str) -> Album | None:
        """
        Returns an album by its hash.
        """
        entry = cls.albummap.get(albumhash)
        if entry is not None:
            return entry.album

    @classmethod
    def get_albums_by_hashes(cls, albumhashes: Iterable[str]) -> list[Album]:
        """
        Returns albums by their hashes.
        """
        return [cls.albummap[albumhash].album for albumhash in albumhashes]

    @classmethod
    def count_albums_by_artisthash(cls, artisthash: str):
        """
        Count albums for the given artisthash.
        """
        master_string = "-".join(a.albumartists_hashes for a in cls.albums)
        return master_string.count(artisthash)

    # @classmethod
    # def album_exists(cls, albumhash: str) -> bool:
    #     """
    #     Checks if an album exists.
    #     """
    #     return albumhash in "-".join([a.albumhash for a in cls.albums])

    @classmethod
    def remove_album(cls, album: Album):
        """
        Removes an album from the store.
        """
        cls.albums.remove(album)

    @classmethod
    def remove_album_by_hash(cls, albumhash: str):
        """
        Removes an album from the store.
        """
        cls.albums = CustomList(a for a in cls.albums if a.albumhash != albumhash)

    @classmethod
    def get_albums_by_artisthash(cls, hash: str):
        """
        Returns all albums by the given artist hash.
        """
        artist = ArtistStore.artistmap.get(hash)

        if not artist:
            return []

        return [cls.albummap[albumhash].album for albumhash in artist.albumhashes]

    @classmethod
    def get_albums_by_artisthashes(cls, hashes: Iterable[str]):
        """
        Returns all albums by the given artist hashes.
        """
        albums = []
        for hash in hashes:
            albums.extend(cls.get_albums_by_artisthash(hash))

        return albums

    @classmethod
    def get_album_tracks(cls, albumhash: str) -> list[Track]:
        """
        Returns all tracks for the given album hash.
        """
        album = cls.albummap.get(albumhash)
        if not album:
            return []

        return TrackStore.get_tracks_by_trackhashes(album.trackhashes)
