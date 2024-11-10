from app.db import Base
from app.db.utils import tracks_to_dataclasses
from app.db.engine import DbEngine
from sqlalchemy import JSON, Integer, String, delete, select
from sqlalchemy.orm import Mapped, mapped_column


from typing import Any, Optional


class TrackTable(Base):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    album: Mapped[str] = mapped_column(String())
    albumartists: Mapped[str] = mapped_column(String())
    albumhash: Mapped[str] = mapped_column(String(), index=True)
    artists: Mapped[str] = mapped_column(String())
    bitrate: Mapped[int] = mapped_column(Integer())
    copyright: Mapped[Optional[str]] = mapped_column(String())
    date: Mapped[int] = mapped_column(Integer(), nullable=True)
    disc: Mapped[int] = mapped_column(Integer())
    duration: Mapped[int] = mapped_column(Integer())
    filepath: Mapped[str] = mapped_column(String(), index=True, unique=True)
    folder: Mapped[str] = mapped_column(String(), index=True)
    genres: Mapped[Optional[str]] = mapped_column(String())
    last_mod: Mapped[float] = mapped_column(Integer())
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

    @classmethod
    def get_tracks_in_path(cls, path: str):
        with DbEngine.manager() as conn:
            result = conn.execute(
                select(TrackTable)
                .where(TrackTable.filepath.contains(path))
                .order_by(TrackTable.last_mod)
            )
            return tracks_to_dataclasses(result.fetchall())

    @classmethod
    def remove_tracks_by_filepaths(cls, filepaths: set[str]):
        with DbEngine.manager(commit=True) as conn:
            conn.execute(delete(TrackTable).where(TrackTable.filepath.in_(filepaths)))
