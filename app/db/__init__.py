import json
from pprint import pprint
from typing import Any, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Integer,
    Row,
    String,
    Tuple,
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
from app.utils.remove_duplicates import remove_duplicates


fullpath = "/home/cwilvx/temp/swingmusic/swing.db"
engine = create_engine(f"sqlite+pysqlite:///{fullpath}", echo=False)


def todict(track: Any):
    return track._asdict()


def todicts(tracks: list[Any]):
    return [todict(track) for track in tracks]


class DbManager:
    def __init__(self):
        self.engine = create_engine(f"sqlite+pysqlite:///{fullpath}", echo=True)
        self.conn = self.engine.connect()

    def __enter__(self):
        return self.conn.execution_options(preserve_rowcount=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


class Base(MappedAsDataclass, DeclarativeBase):
    @classmethod
    def insert_many(cls, items: list[dict[str, Any]]):
        """
        Inserts multiple items into the database.
        """
        with DbManager() as conn:
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
            result = conn.execute(select(cls).offset(start).limit(limit))
            return albums_to_dataclasses(result.fetchall())


class AlbumTable(Base):
    __tablename__ = "album"

    id: Mapped[int] = mapped_column(primary_key=True)
    albumartists: Mapped[list[dict[str, str]]] = mapped_column(JSON(), index=True)
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
    def get_all(cls, start: int, limit: int):
        with DbManager() as conn:
            result = conn.execute(select(AlbumTable).offset(start).limit(limit))
            return albums_to_dataclasses(result.fetchall())

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

            print(albums)
            return albums

    @classmethod
    def get_albums_by_base_title(cls, base_title: str):
        with DbManager() as conn:
            result = conn.execute(
                select(AlbumTable).where(AlbumTable.base_title == base_title)
            )
            return albums_to_dataclasses(result.fetchall())


class TrackTable(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    album: Mapped[str] = mapped_column(String())
    albumartists: Mapped[list[dict[str, str]]] = mapped_column(JSON())
    albumhash: Mapped[str] = mapped_column(String(), index=True)
    artists: Mapped[list[dict[str, str]]] = mapped_column(JSON(), index=True)
    bitrate: Mapped[int] = mapped_column(Integer())
    copyright: Mapped[Optional[str]] = mapped_column(String())
    date: Mapped[int] = mapped_column(Integer())
    disc: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    filepath: Mapped[str] = mapped_column(String(), unique=True)
    folder: Mapped[str] = mapped_column(String(), index=True)
    genre: Mapped[Optional[list[dict[str, str]]]] = mapped_column(JSON())
    last_mod: Mapped[float] = mapped_column(Integer())
    og_album: Mapped[str] = mapped_column(String())
    og_title: Mapped[str] = mapped_column(String())
    title: Mapped[str] = mapped_column(String())
    track: Mapped[int] = mapped_column(Integer())
    trackhash: Mapped[str] = mapped_column(String(), index=True)

    @classmethod
    def get_tracks_by_filepaths(cls, filepaths: list[str]):
        print(filepaths[0])
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable).where(TrackTable.filepath.in_(filepaths))
            )
            return [dict(r) for r in result.mappings().fetchall()]

    @classmethod
    def count_tracks_containing_paths(cls, paths: list[str]):
        results: list[dict[str, int | str]] = []

        with DbManager() as conn:
            for path in paths:
                result = conn.execute(
                    select(TrackTable).where(TrackTable.filepath.contains(path))
                )
                results.append({"path": path, "trackcount": result.all().__len__()})

        return results

    @classmethod
    def get_tracks_by_albumhash(cls, albumhash: str):
        with DbManager() as conn:
            result = conn.execute(
                select(TrackTable).where(TrackTable.albumhash == albumhash)
            )
            tracks = tracks_to_dataclasses(result.fetchall())
            return remove_duplicates(tracks, is_album_tracks=True)


# SECTION: HELPER FUNCTIONS


def album_to_dataclass(album: Row[AlbumTable]):
    return AlbumModel(**album._asdict())


def albums_to_dataclasses(albums: list[Row[AlbumTable]]):
    return [album_to_dataclass(album) for album in albums]


def track_to_dataclass(track: Row[TrackTable]):
    return TrackModel(**track._asdict())


def tracks_to_dataclasses(tracks: list[Row[TrackTable]]):
    return [track_to_dataclass(track) for track in tracks]


Base().metadata.create_all(engine)
