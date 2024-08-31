from sqlalchemy import create_engine, text, Table, Column, Integer, String, MetaData, select
from sqlalchemy.orm import DeclarativeBase

from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

fullpath = "/home/cwilvx/temp/swingmusic/swing.db"
engine = create_engine(f"sqlite+pysqlite:///{fullpath}", echo=True)

class Base(DeclarativeBase):
    pass

class Tracks(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    album: Mapped[str] = mapped_column(String())
    albumartist: Mapped[str] = mapped_column(String())
    copyright: Mapped[Optional[str]]

    def __repr__(self):
        return f"<Tracks(album={self.album}, albumartist={self.albumartist})>"

stmt = select(Tracks.album, Tracks.copyright).where(Tracks.album == "RAVAGE")
print(stmt)

with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(row)

# Base.metadata.create_all(engine)

# metadata = MetaData()
# track_table = Table(
#     "tracks",
#     metadata,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("album", String),
#     Column("albumartist", String),
#     Column("albumhash", String),
#     Column("artist", String),
#     Column("bitrate", Integer),
#     Column("copyright", String),
#     Column("date", Integer),
#     Column("disc", Integer),
#     Column("duration", Integer),
#     Column("filepath", String),
#     Column("folder", String),
#     Column("genre", String),
#     Column("title", String),
#     Column("track", Integer),
#     Column("trackhash", String),
#     Column("last_mod", Integer),
# )

# metadata.create_all(engine)







# with engine.connect() as conn:
#     result = conn.execute(
#         text("SELECT * FROM tracks where trackhash = :trackhash"),
#         {"trackhash": "93acbea22b"},
#     )
#     # print(result.all())

#     for r in result.mappings():
#         print(r["trackhash"])
