from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
from pprint import pprint
from typing import Any, Optional

from memory_profiler import profile
from sqlalchemy import (
    JSON,
    Boolean,
    Integer,
    Row,
    String,
    Tuple,
    and_,
    create_engine,
    insert,
    select,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    MappedAsDataclass,
    sessionmaker,
)

from app.models import Track as TrackModel
from app.models import Album as AlbumModel
from app.models import Artist as ArtistModel
from app.utils.remove_duplicates import remove_duplicates

fullpath = "/home/cwilvx/temp/swingmusic/swing.db"
engine = create_engine(
    f"sqlite+pysqlite:///{fullpath}",
    echo=False,
    max_overflow=0,
    pool_size=5,
)

if not os.path.exists(fullpath):
    os.makedirs(Path(fullpath).parent)

connection = engine.connect()
all_filepaths = list()


def getIndexOfFirstMatch(strings: list[str], prefix: str):
    """
    Find the index of the first path that starts with the given path.

    Uses a binary search algorithm to find the index.
    """

    left = 0
    right = len(strings) - 1

    while left <= right:
        mid = (left + right) // 2

        if strings[mid].startswith(prefix):
            if mid == 0 or not strings[mid - 1].startswith(prefix):
                return mid
            right = mid - 1
        elif strings[mid] < prefix:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def countFilepathsInDir(dirpath: str):
    """
    Return all the filepaths in a directory.
    """
    global all_filepaths
    index = getIndexOfFirstMatch(all_filepaths, dirpath)

    if index == -1:
        return 0

    paths: list[str] = []

    for path in all_filepaths[index:]:
        if path.startswith(dirpath):
            paths.append(path)
        else:
            break

    return len(paths)


class DbManager:
    def __init__(self, commit: bool = False):
        self.commit = commit
        # self.engine = create_engine(f"sqlite+pysqlite:///{fullpath}", echo=True)
        # self.conn = self.engine.connect()
        # pass

    def __enter__(self):
        # return self.conn.execution_options(preserve_rowcount=True)
        return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.commit:
            connection.commit()

        # self.conn.close()


class Base(MappedAsDataclass, DeclarativeBase):
    @classmethod
    def insert_many(cls, items: list[dict[str, Any]]):
        """
        Inserts multiple items into the database.
        """
        with DbManager(commit=True) as conn:
            conn.execute(insert(cls).values(items))

    @classmethod
    def insert_one(cls, item: dict[str, Any]):
        """
        Inserts a single item into the database.
        """
        return cls.insert_many([item])

    @classmethod
    def get_all(cls):
        """
        Returns all the items from the database.
        """
        with DbManager() as conn:
            result = conn.execute(select(cls))
            return result.fetchall()


class ArtistTable(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(primary_key=True)
    albumcount: Mapped[int] = mapped_column(Integer())
    artisthash: Mapped[str] = mapped_column(String(), unique=True, index=True)
    created_date: Mapped[int] = mapped_column(Integer())
    date: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    genres: Mapped[str] = mapped_column(JSON())
    name: Mapped[str] = mapped_column(String(), index=True)
    trackcount: Mapped[int] = mapped_column(Integer())
    is_favorite: Mapped[Optional[bool]] = mapped_column(Boolean())

    @classmethod
    def get_all(cls, start: int, limit: int):
        with DbManager() as conn:
            if start == 0:
                result = conn.execute(select(cls))
            else:
                result = conn.execute(select(cls).offset(start).limit(limit))

            all = result.fetchall()
            return artists_to_dataclasses(all), len(all)

    @classmethod
    def get_artist_by_hash(cls, artisthash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(ArtistTable).where(ArtistTable.artisthash == artisthash)
            )
            return artist_to_dataclass(result.fetchone())


class AlbumTable(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    albumartists: Mapped[list[dict[str, str]]] = mapped_column(JSON(), index=True)
    artisthashes: Mapped[list[str]] = mapped_column(JSON(), index=True)
    albumhash: Mapped[str] = mapped_column(String(), unique=True, index=True)
    base_title: Mapped[str] = mapped_column(String())
    color: Mapped[Optional[str]] = mapped_column(String())
    created_date: Mapped[int] = mapped_column(Integer())
    date: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    genres: Mapped[str] = mapped_column(JSON())
    og_title: Mapped[str] = mapped_column(String())
    title: Mapped[str] = mapped_column(String())
    trackcount: Mapped[int] = mapped_column(Integer())

    @classmethod
    def get_album_by_albumhash(cls, hash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(AlbumTable).where(AlbumTable.albumhash == hash)
            )
            album = result.fetchone()

            if album:
                return album_to_dataclass(album)

    @classmethod
    def get_albums_by_hash(cls, hashes: set[str]):
        with DbManager() as conn:
            result = conn.execute(
                select(AlbumTable).where(AlbumTable.albumhash.in_(hashes))
            )
            return albums_to_dataclasses(result.fetchall())

    @classmethod
    def get_all(cls, start: int, limit: int):
        with DbManager() as conn:
            if start == 0:
                result = conn.execute(select(AlbumTable))
            else:
                result = conn.execute(select(AlbumTable).offset(start).limit(limit))

            all = result.fetchall()

            return albums_to_dataclasses(all)[:limit], len(all)

    @classmethod
    def get_albums_by_artisthashes(cls, artisthashes: list[dict[str, str]]):
        with DbManager() as conn:
            albums: list[AlbumModel] = []

            for artist in artisthashes:
                result = conn.execute(
                    # NOTE: The artist dict keys need to in the same order they appear in the db for this to work!
                    select(AlbumTable).where(AlbumTable.albumartists.contains(artist))
                )
                albums.extend(albums_to_dataclasses(result.fetchall()))

            return albums

    @classmethod
    def get_albums_by_base_title(cls, base_title: str):
        with DbManager() as conn:
            result = conn.execute(
                select(AlbumTable).where(AlbumTable.base_title == base_title)
            )
            return albums_to_dataclasses(result.fetchall())

    @classmethod
    def get_albums_by_artisthash(cls, artisthash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(AlbumTable).where(AlbumTable.artisthashes.contains(artisthash))
            )
            return albums_to_dataclasses(result.all())


class TrackTable(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    album: Mapped[str] = mapped_column(String())
    albumartists: Mapped[list[dict[str, str]]] = mapped_column(JSON())
    albumhash: Mapped[str] = mapped_column(String(), index=True)
    artisthashes: Mapped[list[str]] = mapped_column(JSON(), index=True)
    artists: Mapped[list[dict[str, str]]] = mapped_column(JSON(), index=True)
    bitrate: Mapped[int] = mapped_column(Integer())
    copyright: Mapped[Optional[str]] = mapped_column(String())
    date: Mapped[int] = mapped_column(Integer())
    disc: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    filepath: Mapped[str] = mapped_column(String(), index=True, unique=True)
    folder: Mapped[str] = mapped_column(String(), index=True)
    genre: Mapped[Optional[list[dict[str, str]]]] = mapped_column(JSON())
    last_mod: Mapped[float] = mapped_column(Integer())
    og_album: Mapped[str] = mapped_column(String())
    og_title: Mapped[str] = mapped_column(String())
    title: Mapped[str] = mapped_column(String())
    track: Mapped[int] = mapped_column(Integer())
    trackhash: Mapped[str] = mapped_column(String(), index=True)
    extra: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON())

    @classmethod
    def get_tracks_by_filepaths(cls, filepaths: list[str]):
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable).where(TrackTable.filepath.in_(filepaths))
            )
            return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def count_tracks_containing_paths(cls, paths: list[str]):
        results: list[dict[str, int | str]] = []

        with ThreadPoolExecutor() as executor:
            res = executor.map(countFilepathsInDir, paths)
            results = [
                {"path": path, "trackcount": count} for path, count in zip(paths, res)
            ]

        return results

    @classmethod
    def get_tracks_by_albumhash(cls, albumhash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable).where(TrackTable.albumhash == albumhash)
            )
            tracks = tracks_to_dataclasses(result.fetchall())
            return remove_duplicates(tracks, is_album_tracks=True)

    @classmethod
    def get_track_by_trackhash(cls, hash: str, filepath: str = ""):
        with DbManager() as conn:
            if filepath:
                result = conn.execute(
                    select(TrackTable)
                    .where(
                        and_(
                            TrackTable.trackhash == hash,
                            TrackTable.filepath == filepath,
                        )
                    )
                    .order_by(TrackTable.bitrate.desc())
                )
            else:
                result = conn.execute(
                    select(TrackTable).where(TrackTable.trackhash == hash)
                )

            track = result.fetchone()

            if track:
                return track_to_dataclass(track)

    @classmethod
    def get_tracks_by_artisthash(cls, artisthash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable).where(TrackTable.artists.contains(artisthash))
            )
            return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def get_tracks_in_path(cls, path: str):
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable)
                .where(TrackTable.filepath.contains(path))
                .order_by(TrackTable.last_mod)
            )
            return tracks_to_dataclasses(result.fetchall())


all_tracks = TrackTable.get_all()

for track in all_tracks:
    all_filepaths.append(track.filepath)

all_filepaths.sort()

# print("files in path: ",getFilepathsInDir("/home/cwilvx/Music/").__len__())


# SECTION: Userdata database
class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True)
    firstname: Mapped[Optional[str]] = mapped_column(String())
    lastname: Mapped[Optional[str]] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    email: Mapped[Optional[str]] = mapped_column(String())
    image: Mapped[Optional[str]] = mapped_column(String())
    roles: Mapped[list[str]] = mapped_column(JSON(), default_factory=lambda: ["user"])
    extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON(), default_factory=dict
    )


# SECTION: HELPER FUNCTIONS


def artist_to_dataclass(artist: Any):
    return ArtistModel(**artist._asdict())


def artists_to_dataclasses(artists: Any):
    return [artist_to_dataclass(artist) for artist in artists]


def album_to_dataclass(album: Any):
    return AlbumModel(**album._asdict())


def albums_to_dataclasses(albums: Any):
    return [album_to_dataclass(album) for album in albums]


def track_to_dataclass(track: Any):
    return TrackModel(**track._asdict())


def tracks_to_dataclasses(tracks: Any):
    return [track_to_dataclass(track) for track in tracks]


Base().metadata.create_all(engine)
