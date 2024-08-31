from app.db import Base
from app.db.utils import tracks_to_dataclasses
from app.db.engine import DbEngine
from sqlalchemy import JSON, Integer, String, delete, select
from sqlalchemy.orm import Mapped, mapped_column


from typing import Any, Optional


# def create_all():
#     """
#     Create all the tables defined in this file.

#     NOTE: We need this function because the MasterBase does not collect
#     the tables defined here (as they are grand-children of the MasterBase)
#     """
#     Base.metadata.create_all(DbEngine.engine)


# class Base(MasterBase, DeclarativeBase):
#     pass
# @classmethod
# def get_all_hashes(cls, create_date: int | None = None):
#     with DbEngine.manager() as conn:
#         if create_date:
#             if cls.__tablename__ == "track":
#                 stmt = select(TrackTable.trackhash).where(
#                     cls.last_mod < create_date
#                 )
#             elif cls.__tablename__ == "album":
#                 stmt = select(AlbumTable.albumhash).where(
#                     cls.created_date < create_date
#                 )
#             elif cls.__tablename__ == "artist":
#                 stmt = select(ArtistTable.artisthash).where(
#                     cls.created_date < create_date
#                 )
#         else:
#             if cls.__tablename__ == "track":
#                 stmt = select(TrackTable.trackhash)
#             elif cls.__tablename__ == "album":
#                 stmt = select(AlbumTable.albumhash)
#             elif cls.__tablename__ == "artist":
#                 stmt = select(ArtistTable.artisthash)

#         result = conn.execute(stmt)
#         return {row[0] for row in result.fetchall()}

# @classmethod
# def set_is_favorite(cls, hash: str, is_favorite: bool):
#     """
#     Set the 'is_favorite' flag for a specific hash.

#     Args:
#         hash (str): The hash value.
#         is_favorite (bool): The value of the 'is_favorite' flag.
#     """
#     with DbEngine.manager(commit=True) as conn:
#         if cls.__tablename__ == "track":
#             stmt = (
#                 update(cls)
#                 .where(TrackTable.trackhash == hash)
#                 .values(is_favorite=is_favorite)
#             )
#         elif cls.__tablename__ == "album":
#             stmt = (
#                 update(cls)
#                 .where(AlbumTable.albumhash == hash)
#                 .values(is_favorite=is_favorite)
#             )
#         elif cls.__tablename__ == "artist":
#             stmt = (
#                 update(cls)
#                 .where(ArtistTable.artisthash == hash)
#                 .values(is_favorite=is_favorite)
#             )

#         conn.execute(stmt)

# @classmethod
# def increment_scrobblecount(
#     cls, table: Any, field: Any, hash: str, duration: int, timestamp: int
# ):
#     cls.execute(
#         update(table)
#         .where(field == hash)
#         .values(
#             playcount=table.playcount + 1,
#             playduration=table.playduration + duration,
#             lastplayed=timestamp,
#         ),
#         commit=True,
#     )


class TrackTable(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    album: Mapped[str] = mapped_column(String())
    albumartists: Mapped[str] = mapped_column(String())
    albumhash: Mapped[str] = mapped_column(String(), index=True)
    # artisthashes: Mapped[list[str]] = mapped_column(JSON(), index=True)
    artists: Mapped[str] = mapped_column(String())
    bitrate: Mapped[int] = mapped_column(Integer())
    copyright: Mapped[Optional[str]] = mapped_column(String())
    date: Mapped[int] = mapped_column(Integer(), nullable=True)
    disc: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    filepath: Mapped[str] = mapped_column(String(), index=True, unique=True)
    folder: Mapped[str] = mapped_column(String(), index=True)
    # genrehashes: Mapped[list[str]] = mapped_column(JSON(), index=True)
    genres: Mapped[Optional[str]] = mapped_column(String())
    last_mod: Mapped[float] = mapped_column(Integer())
    # og_album: Mapped[str] = mapped_column(String())
    # og_title: Mapped[str] = mapped_column(String())
    title: Mapped[str] = mapped_column(String())
    track: Mapped[int] = mapped_column(Integer())
    trackhash: Mapped[str] = mapped_column(String(), index=True)
    lastplayed: Mapped[int] = mapped_column(Integer(), default=0)
    playcount: Mapped[int] = mapped_column(Integer(), default=0)
    playduration: Mapped[int] = mapped_column(Integer(), default=0)
    extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSON(), default_factory=dict
    )

    @classmethod
    def get_all(cls):
        with DbEngine.manager() as conn:
            result = conn.execute(select(cls))
            return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def get_tracks_by_filepaths(cls, filepaths: list[str]):
        with DbEngine.manager() as conn:
            result = conn.execute(
                select(TrackTable)
                .where(TrackTable.filepath.in_(filepaths))
                .order_by(TrackTable.last_mod)
            )
            return tracks_to_dataclasses(result.fetchall())

    # @classmethod
    # def get_tracks_by_albumhash(cls, albumhash: str):
    #     with DbEngine.manager() as conn:
    #         result = conn.execute(
    #             select(TrackTable).where(TrackTable.albumhash == albumhash)
    #         )
    #         tracks = tracks_to_dataclasses(result.fetchall())
    #         return remove_duplicates(tracks, is_album_tracks=True)

    # @classmethod
    # def get_track_by_trackhash(cls, hash: str, filepath: str = ""):
    #     with DbEngine.manager() as conn:
    #         if filepath:
    #             result = conn.execute(
    #                 select(TrackTable)
    #                 .where(
    #                     (TrackTable.trackhash == hash)
    #                     & (TrackTable.filepath == filepath),
    #                 )
    #                 .order_by(TrackTable.bitrate.desc())
    #             )
    #         else:
    #             result = conn.execute(
    #                 select(TrackTable).where(TrackTable.trackhash == hash)
    #             )

    #         track = result.fetchone()

    #         if track:
    #             return track_to_dataclass(track)

    # @classmethod
    # def get_tracks_by_artisthash(cls, artisthash: str):
    #     with DbEngine.manager() as conn:
    #         result = conn.execute(
    #             select(TrackTable).where(TrackTable.artists.contains(artisthash))
    #         )
    #         return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def get_tracks_in_path(cls, path: str):
        with DbEngine.manager() as conn:
            result = conn.execute(
                select(TrackTable)
                .where(TrackTable.filepath.contains(path))
                .order_by(TrackTable.last_mod)
            )
            return tracks_to_dataclasses(result.fetchall())

    # @classmethod
    # def get_tracks_by_trackhashes(cls, hashes: Iterable[str], limit: int | None = None):
    #     with DbEngine.manager() as conn:
    #         result = conn.execute(
    #             select(TrackTable)
    #             .where(TrackTable.trackhash.in_(hashes))
    #             .group_by(TrackTable.trackhash)
    #             .limit(limit)
    #         )
    #         tracks = tracks_to_dataclasses(result.fetchall())

    #         # order the tracks in the same order as the hashes
    #         if type(hashes) == list:
    #             return sorted(tracks, key=lambda x: hashes.index(x.trackhash))

    #         return tracks

    # @classmethod
    # def get_recently_added(cls, start: int, limit: int):
    #     with DbEngine.manager() as conn:
    #         result = conn.execute(
    #             select(TrackTable)
    #             .order_by(TrackTable.last_mod.desc())
    #             .offset(start)
    #             .limit(limit)
    #         )

    #         return tracks_to_dataclasses(result.fetchall())

    @classmethod
    # def get_recently_played(cls, limit: int):
    #     result = cls.execute(
    #         select(cls)
    #         .group_by(cls.trackhash)
    #         .order_by(cls.lastplayed.desc())
    #         .limit(limit)
    #     )
    #     return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def remove_tracks_by_filepaths(cls, filepaths: set[str]):
        with DbEngine.manager(commit=True) as conn:
            conn.execute(delete(TrackTable).where(TrackTable.filepath.in_(filepaths)))

    # @classmethod
    # def increment_playcount(cls, trackhash: str, duration: int, timestamp: int):
    #     cls.increment_scrobblecount(
    #         TrackTable, TrackTable.trackhash, trackhash, duration, timestamp
    #     )

    # @classmethod
    # def update_artist_separators(cls, separators: set[str]):
    #     tracks = cls.get_all()

    #     with DbEngine.manager(commit=True) as conn:
    #         for track in tracks:
    #             track.split_artists(separators)
    #             conn.execute(
    #                 update(cls)
    #                 .where(cls.trackhash == track.trackhash)
    #                 .values(artists=track.artists, artisthashes=track.artisthashes)
    #             )


# class AlbumTable(Base):
#     __tablename__ = "album"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     albumartists: Mapped[list[dict[str, str]]] = mapped_column(JSON(), index=True)
#     artisthashes: Mapped[list[str]] = mapped_column(JSON(), index=True)
#     albumhash: Mapped[str] = mapped_column(String(), unique=True, index=True)
#     base_title: Mapped[str] = mapped_column(String())
#     color: Mapped[Optional[str]] = mapped_column(String())
#     created_date: Mapped[int] = mapped_column(Integer())
#     date: Mapped[int] = mapped_column(Integer())
#     duration: Mapped[int] = mapped_column(Integer())
#     genrehashes: Mapped[list[str]] = mapped_column(JSON(), nullable=True, index=True)
#     genres: Mapped[str] = mapped_column(JSON())
#     og_title: Mapped[str] = mapped_column(String())
#     title: Mapped[str] = mapped_column(String())
#     trackcount: Mapped[int] = mapped_column(Integer())
#     lastplayed: Mapped[int] = mapped_column(Integer(), default=0)
#     playcount: Mapped[int] = mapped_column(Integer(), default=0)
#     playduration: Mapped[int] = mapped_column(Integer(), default=0)
#     extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
#         JSON(), default_factory=dict
#     )

#     @classmethod
#     def get_all(cls):
#         with DbEngine.manager() as conn:
#             result = conn.execute(select(AlbumTable))
#             all = result.fetchall()
#             return albums_to_dataclasses(all)

#     @classmethod
#     def get_album_by_albumhash(cls, hash: str):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(AlbumTable).where(AlbumTable.albumhash == hash)
#             )
#             album = result.fetchone()

#             if album:
#                 return album_to_dataclass(album)

#     @classmethod
#     def get_albums_by_albumhashes(cls, hashes: Iterable[str], limit: int | None = None):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(AlbumTable).where(AlbumTable.albumhash.in_(hashes)).limit(limit)
#             )
#             albums = albums_to_dataclasses(result.fetchall())

#             # order the albums in the same order as the hashes
#             if type(hashes) == list:
#                 return sorted(albums, key=lambda x: hashes.index(x.albumhash))

#             return albums

#     @classmethod
#     def get_albums_by_artisthashes(cls, artisthashes: list[str]):
#         with DbEngine.manager() as conn:
#             albums: dict[str, list[AlbumModel]] = {}

#             for artist in artisthashes:
#                 result = conn.execute(
#                     select(AlbumTable).where(AlbumTable.artisthashes.contains(artist))
#                 )
#                 albums[artist] = albums_to_dataclasses(result.fetchall())

#             return albums

#     @classmethod
#     def get_albums_by_base_title(cls, base_title: str):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(AlbumTable).where(AlbumTable.base_title == base_title)
#             )
#             return albums_to_dataclasses(result.fetchall())

#     @classmethod
#     def get_albums_by_artisthash(cls, artisthash: str):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(AlbumTable).where(AlbumTable.artisthashes.contains(artisthash))
#             )
#             return albums_to_dataclasses(result.all())

#     @classmethod
#     def increment_playcount(cls, albumhash: str, duration: int, timestamp: int):
#         return cls.increment_scrobblecount(
#             AlbumTable, AlbumTable.albumhash, albumhash, duration, timestamp
#         )


# class ArtistTable(Base):
#     __tablename__ = "artist"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     albumcount: Mapped[int] = mapped_column(Integer())
#     artisthash: Mapped[str] = mapped_column(String(), unique=True, index=True)
#     created_date: Mapped[int] = mapped_column(Integer())
#     date: Mapped[int] = mapped_column(Integer())
#     duration: Mapped[int] = mapped_column(Integer())
#     genrehashes: Mapped[list[str]] = mapped_column(JSON(), nullable=True, index=True)
#     genres: Mapped[str] = mapped_column(JSON())
#     name: Mapped[str] = mapped_column(String(), index=True)
#     trackcount: Mapped[int] = mapped_column(Integer())
#     lastplayed: Mapped[int] = mapped_column(Integer(), default=0)
#     playcount: Mapped[int] = mapped_column(Integer(), default=0)
#     playduration: Mapped[int] = mapped_column(Integer(), default=0)
#     extra: Mapped[Optional[dict[str, Any]]] = mapped_column(
#         JSON(), default_factory=dict
#     )

#     @classmethod
#     def get_all(cls):
#         with DbEngine.manager() as conn:
#             result = conn.execute(select(cls))
#             all = result.fetchall()
#             return artists_to_dataclasses(all)

#     @classmethod
#     def get_artist_by_hash(cls, artisthash: str):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(ArtistTable).where(ArtistTable.artisthash == artisthash)
#             )
#             return artist_to_dataclass(result.fetchone())

#     @classmethod
#     def get_artisthashes_not_in(cls, artisthashes: list[str]):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(ArtistTable.artisthash, ArtistTable.name).where(
#                     ~ArtistTable.artisthash.in_(artisthashes)
#                 )
#             )
#             return [{"artisthash": row[0], "name": row[1]} for row in result.fetchall()]

#     @classmethod
#     def get_artists_by_artisthashes(
#         cls, hashes: Iterable[str], limit: int | None = None
#     ):
#         with DbEngine.manager() as conn:
#             result = conn.execute(
#                 select(ArtistTable)
#                 .where(ArtistTable.artisthash.in_(hashes))
#                 .limit(limit)
#             )
#             return artists_to_dataclasses(result.fetchall())

#     @classmethod
#     def increment_playcount(
#         cls, artisthashes: list[str], duration: int, timestamp: int
#     ):
#         cls.execute(
#             update(cls)
#             .where(ArtistTable.artisthash.in_(artisthashes))
#             .values(
#                 playcount=ArtistTable.playcount + 1,
#                 playduration=ArtistTable.playduration + duration,
#                 lastplayed=timestamp,
#             ),
#             commit=True,
#         )
