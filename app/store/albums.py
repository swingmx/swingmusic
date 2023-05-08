import json
import random

from tqdm import tqdm

from app.models import Album, Track
from app.db.sqlite.albums import SQLiteAlbumMethods as aldb
from .tracks import TrackStore
from ..utils.hashing import create_hash


class AlbumStore:
    albums: list[Album] = []

    @staticmethod
    def create_album(track: Track):
        """
        Creates album object from a track
        """
        return Album(
            albumhash=track.albumhash,
            albumartists=track.albumartist,  # type: ignore
            title=track.album,
        )

    @classmethod
    def load_albums(cls):
        """
        Loads all albums from the database into the store.
        """

        cls.albums = []

        albumhashes = set(t.albumhash for t in TrackStore.tracks)

        for albumhash in tqdm(albumhashes, desc="Loading albums"):
            for track in TrackStore.tracks:
                if track.albumhash == albumhash:
                    cls.albums.append(cls.create_album(track))
                    break

        db_albums: list[tuple] = aldb.get_all_albums()

        for album in tqdm(db_albums, desc="Mapping album colors"):
            albumhash = album[1]
            colors = json.loads(album[2])

            for _al in cls.albums:
                if _al.albumhash == albumhash:
                    _al.set_colors(colors)
                    break

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

        albums = [album for album in cls.albums if artisthash in album.albumartists_hashes]

        albums = [album for album in albums if create_hash(album.base_title) != create_hash(exclude)]

        if len(albums) > limit:
            random.shuffle(albums)

        # TODO: Merge this with `cls.get_albums_by_artisthash()`
        return albums[:limit]

    @classmethod
    def get_album_by_hash(cls, albumhash: str) -> Album | None:
        """
        Returns an album by its hash.
        """
        try:
            return [a for a in cls.albums if a.albumhash == albumhash][0]
        except IndexError:
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
        return [album for album in cls.albums if artisthash in album.albumartists_hashes]

    @classmethod
    def count_albums_by_artisthash(cls, artisthash: str):
        """
        Count albums for the given artisthash.
        """
        albumartists = [a.albumartists for a in cls.albums]
        artisthashes = []

        for artist in albumartists:
            artisthashes.extend([a.artisthash for a in artist])  # type: ignore

        master_string = "-".join(artisthashes)

        return master_string.count(artisthash)

    @classmethod
    def album_exists(cls, albumhash: str) -> bool:
        """
        Checks if an album exists.
        """
        return albumhash in "-".join([a.albumhash for a in cls.albums])

    @classmethod
    def remove_album_by_hash(cls, albumhash: str):
        """
        Removes an album from the store.
        """
        cls.albums = [a for a in cls.albums if a.albumhash != albumhash]
