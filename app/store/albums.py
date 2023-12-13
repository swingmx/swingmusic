from itertools import groupby
import json
import random

from app.db.sqlite.albumcolors import SQLiteAlbumMethods as aldb
from app.models import Album, Track
from app.utils.remove_duplicates import remove_duplicates

from ..utils.hashing import create_hash
from .tracks import TrackStore
from app.utils.progressbar import tqdm

ALBUM_LOAD_KEY = ""


class AlbumStore:
    albums: list[Album] = []

    @staticmethod
    def create_album(track: Track):
        """
        Creates album object from a track
        """
        return Album(
            albumhash=track.albumhash,
            albumartists=track.albumartists,  # type: ignore
            title=track.og_album,
        )

    @classmethod
    def load_albums(cls, instance_key: str):
        """
        Loads all albums from the database into the store.
        """
        global ALBUM_LOAD_KEY
        ALBUM_LOAD_KEY = instance_key

        cls.albums = []

        print("Loading albums... ", end="")
        tracks = remove_duplicates(TrackStore.tracks)
        tracks = sorted(tracks, key=lambda t: t.albumhash)
        grouped = groupby(tracks, lambda t: t.albumhash)

        for albumhash, tracks in grouped:
            tracks = list(tracks)
            sample = tracks[0]

            if sample is None:
                continue

            count = len(list(tracks))
            duration = sum(t.duration for t in tracks)
            created_date = min(t.created_date for t in tracks)

            album = AlbumStore.create_album(sample)

            album.get_date_from_tracks(tracks)
            album.set_count(count)
            album.set_duration(duration)
            album.set_created_date(created_date)

            cls.albums.append(album)

        db_albums: list[tuple] = aldb.get_all_albums()

        for album in db_albums:
            albumhash = album[1]
            colors = json.loads(album[2])

            for _al in cls.albums:
                if _al.albumhash == albumhash:
                    _al.set_colors(colors)
                    break

        print("Done!")

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

        albums = [
            album for album in cls.albums if artisthash in album.albumartists_hashes
        ]

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
        for album in cls.albums:
            if album.albumhash == albumhash:
                return album

        return None

    @classmethod
    def get_albums_by_hashes(cls, albumhashes: list[str]) -> list[Album]:
        """
        Returns albums by their hashes.
        """
        albums_str = "-".join(albumhashes)
        albums = [a for a in cls.albums if a.albumhash in albums_str]

        # sort albums by the order of the hashes
        albums.sort(key=lambda x: albumhashes.index(x.albumhash))
        return albums

    @classmethod
    def get_albums_by_artisthash(cls, artisthash: str) -> list[Album]:
        """
        Returns all albums by the given artist.
        """
        return [
            album for album in cls.albums if artisthash in album.albumartists_hashes
        ]

    @classmethod
    def count_albums_by_artisthash(cls, artisthash: str):
        """
        Count albums for the given artisthash.
        """
        master_string = "-".join(a.albumartists_hashes for a in cls.albums)
        return master_string.count(artisthash)

    @classmethod
    def album_exists(cls, albumhash: str) -> bool:
        """
        Checks if an album exists.
        """
        return albumhash in "-".join([a.albumhash for a in cls.albums])

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
        cls.albums = [a for a in cls.albums if a.albumhash != albumhash]
