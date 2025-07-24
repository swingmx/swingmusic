from dataclasses import asdict
import datetime
import json
from typing import Any, Iterable, Literal
from sqlalchemy import (
    JSON,
    Boolean,
    ForeignKey,
    Integer,
    String,
    and_,
    delete,
    func,
    insert,
    select,
    update,
)

from sqlalchemy.orm import Mapped, mapped_column

from swingmusic.db.engine import DbEngine
from swingmusic.db.utils import (
    favorite_to_dataclass,
    favorites_to_dataclass,
    playlist_to_dataclass,
    plugin_to_dataclass,
    similar_artist_to_dataclass,
    tracklog_to_dataclass,
    user_to_dataclass,
)

from swingmusic.db import Base
from swingmusic.models.mix import Mix
from swingmusic.utils.auth import get_current_userid, hash_password


class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(), nullable=True)
    password: Mapped[str] = mapped_column(String())
    username: Mapped[str] = mapped_column(String(), index=True)
    roles: Mapped[list[str]] = mapped_column(JSON(), default_factory=lambda: [])
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def get_all(cls):
        result = cls.execute(select(cls))

        for i in next(result).scalars():
            yield user_to_dataclass(i)

    @classmethod
    def insert_default_user(cls):
        user = {
            "username": "admin",
            "password": hash_password("admin"),
            "roles": ["admin"],
        }

        return cls.insert_one(user)

    @classmethod
    def insert_guest_user(cls):
        user = {
            "username": "guest",
            "password": hash_password("guest"),
            "roles": ["guest"],
        }

        return cls.insert_one(user)

    @classmethod
    def get_by_id(cls, id: int):
        result = cls.execute(select(cls).where(cls.id == id))
        res = next(result).scalar()

        if res:
            return user_to_dataclass(res)

    @classmethod
    def get_by_username(cls, username: str):
        res = cls.execute(select(cls).where(cls.username == username))
        res = next(res).scalar()

        if res:
            return user_to_dataclass(res)

    @classmethod
    def update_one(cls, user: dict[str, Any]):
        return next(
            cls.execute(
                update(cls).where(cls.id == user["id"]).values(user), commit=True
            )
        )

    @classmethod
    def remove_by_username(cls, username: str):
        return next(
            cls.execute(delete(cls).where(cls.username == username), commit=True)
        )


class PluginTable(Base):
    __tablename__ = "plugin"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), unique=True)
    active: Mapped[bool] = mapped_column(Boolean())
    settings: Mapped[dict[str, Any]] = mapped_column(JSON())
    extra: Mapped[dict[str, Any]] = mapped_column(JSON(), nullable=True)

    @classmethod
    def get_all(cls):
        result = cls.execute(select(cls))

        for i in next(result).scalars():
            yield plugin_to_dataclass(i)

    @classmethod
    def activate(cls, name: str, value: bool):
        return next(
            cls.execute(
                update(cls).where(cls.name == name).values(active=value), commit=True
            )
        )

    @classmethod
    def get_by_name(cls, name: str):
        result = cls.execute(select(cls).where(cls.name == name))
        res = next(result).scalar()

        if res:
            return plugin_to_dataclass(res)

    @classmethod
    def update_settings(cls, name: str, settings: dict[str, Any]):
        return next(
            cls.execute(
                update(cls).where(cls.name == name).values(settings=settings),
                commit=True,
            )
        )


class SimilarArtistTable(Base):
    __tablename__ = "notlastfm_similar_artists"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    artisthash: Mapped[str] = mapped_column(String(), index=True)
    similar_artists: Mapped[dict[str, str]] = mapped_column(JSON())

    @classmethod
    def get_all(cls):
        result = cls.execute(select(cls).execution_options(yield_per=100))

        for i in next(result).scalars():
            yield similar_artist_to_dataclass(i)

    @classmethod
    def exists(cls, artisthash: str):
        """
        Check whether an artisthash exists in the database.
        """

        with DbEngine.manager() as conn:
            result = conn.execute(
                select(cls.artisthash)
                .where(cls.artisthash == artisthash)
                .execution_options(yield_per=100)
            )

            return len(result.scalars().all()) > 0

    @classmethod
    def get_by_hash(cls, artisthash: str):
        """
        Get a single artist by hash.
        """
        result = cls.execute(select(cls).where(cls.artisthash == artisthash))
        res = next(result).scalar()

        if res:
            return similar_artist_to_dataclass(res)


class FavoritesTable(Base):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(String(), unique=True)
    type: Mapped[str] = mapped_column(String(), index=True)
    timestamp: Mapped[int] = mapped_column(Integer(), index=True)
    userid: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade"), default=1, index=True
    )
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def get_all(cls, with_user: bool = False):
        with DbEngine.manager() as conn:
            if with_user:
                result = conn.execute(
                    select(cls).where(cls.userid == get_current_userid())
                )
            else:
                result = conn.execute(select(cls))

            for i in result.scalars():
                yield favorite_to_dataclass(i)

    @classmethod
    def insert_item(cls, item: dict[str, Any]):
        # guard against hash collisions for different item types
        item["hash"] = f"{item['type']}_{item['hash']}"

        if item.get("timestamp") is None:
            item["timestamp"] = int(datetime.datetime.now().timestamp())

        if item.get("userid") is None:
            item["userid"] = get_current_userid()

        return next(cls.execute(insert(cls).values(item), commit=True))

    @classmethod
    def remove_item(cls, item: dict[str, Any]):
        return next(
            cls.execute(
                delete(cls).where(
                    (cls.hash == item["hash"])
                    | (cls.hash == f"{item['type']}_{item['hash']}")
                ),
                commit=True,
            )
        )

    @classmethod
    def check_exists(cls, hash: str, type: str):
        result = cls.execute(
            select(cls).where((cls.hash == hash) | (cls.hash == f"{type}_{hash}"))
        )

        return next(result).scalar() is not None

    @classmethod
    def get_by_hash(cls, hash: str, type: str):
        result = cls.execute(
            select(cls).where((cls.hash == hash) | (cls.hash == f"{type}_{hash}"))
        )

        return next(result).scalars().all()

    @classmethod
    def get_all_of_type(cls, type: str, start: int, limit: int):
        result = cls.execute(
            select(cls)
            # .select_from(join(table, cls, field == cls.hash))
            .where(and_(cls.type == type, cls.userid == get_current_userid()))
            .order_by(cls.timestamp.desc())
            .offset(start)
            # INFO: If start is 0, fetch all so we can get the total count
            .limit(limit if start != 0 else None)
        )

        res = next(result).scalars().all()

        if start == 0:
            # if limit == -1, return all
            if limit == -1:
                limit = len(res)

            return res[:limit], len(res)

        return res, -1

    @classmethod
    def get_fav_tracks(cls, start: int, limit: int):
        result, total = cls.get_all_of_type("track", start, limit)
        return favorites_to_dataclass(result), total

    @classmethod
    def get_fav_albums(cls, start: int, limit: int):
        result, total = cls.get_all_of_type("album", start, limit)
        return favorites_to_dataclass(result), total

    @classmethod
    def get_fav_artists(cls, start: int, limit: int):
        result, total = cls.get_all_of_type("artist", start, limit)
        return favorites_to_dataclass(result), total

    @classmethod
    def count_favs_in_period(cls, start_time: int, end_time: int):
        result = cls.execute(
            select(func.count(cls.id))
            .where((cls.userid == get_current_userid()))
            .where(and_(cls.timestamp >= start_time, cls.timestamp <= end_time))
        )

        res = next(result).scalar()

        if res:
            return res

        return 0

    @classmethod
    def count_tracks(cls):
        result = cls.execute(select(func.count(cls.id)).where(cls.type == "track"))

        return next(result).scalar()

    @classmethod
    def get_last_trackhash(cls):
        result = cls.execute(
            select(cls.hash).where(cls.type == "track").order_by(cls.timestamp.desc())
        )

        return next(result).scalar()


class ScrobbleTable(Base):
    __tablename__ = "scrobble"

    id: Mapped[int] = mapped_column(primary_key=True)
    trackhash: Mapped[str] = mapped_column(String(), index=True)
    duration: Mapped[int] = mapped_column(Integer())
    timestamp: Mapped[int] = mapped_column(Integer())
    source: Mapped[str] = mapped_column(String())
    userid: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade"), index=True
    )
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def add(cls, item: dict[str, Any]):
        if item.get("userid") is None:
            item["userid"] = get_current_userid()

        return cls.insert_one(item)

    @classmethod
    def get_all(cls, start: int, limit: int | None = None, userid: int | None = None):
        result = cls.execute(
            select(cls)
            .where(cls.userid == (userid if userid else get_current_userid()))
            .order_by(cls.timestamp.desc())
            .offset(start)
            .limit(limit)
            .execution_options(yield_per=100)
        )

        for i in next(result).scalars():
            yield tracklog_to_dataclass(i)

    @classmethod
    def get_all_in_period(cls, start_time: int, end_time: int, userid: int | None):
        # UserId will be None if function is called from the API
        # In that case, we use the request userid
        if userid is None:
            userid = get_current_userid()

        result = cls.execute(
            select(cls)
            .where(cls.userid == userid)
            .where(and_(cls.timestamp >= start_time, cls.timestamp <= end_time))
            .order_by(cls.timestamp.desc())
            .execution_options(yield_per=100)
        )

        for i in next(result).scalars():
            yield tracklog_to_dataclass(i)

    @classmethod
    def get_last_entry(cls, userid: int):
        result = cls.execute(
            select(cls).where(cls.userid == userid).order_by(cls.timestamp.desc())
        )
        res = next(result).scalar()

        if res:
            return tracklog_to_dataclass(res)


class PlaylistTable(Base):
    __tablename__ = "playlist"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), index=True)
    last_updated: Mapped[int] = mapped_column(Integer())
    image: Mapped[str] = mapped_column(String(), nullable=True)
    userid: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade")
    )
    settings: Mapped[dict[str, Any]] = mapped_column(JSON())
    trackhashes: Mapped[list[str]] = mapped_column(JSON(), default_factory=list)
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def get_all(cls, current_user: bool = True):
        if current_user:
            result = cls.execute(
                select(cls)
                .where(cls.userid == get_current_userid())
                .execution_options(yield_per=100)
            )
        else:
            result = cls.execute(select(cls).execution_options(yield_per=100))

        for i in next(result).scalars():
            yield playlist_to_dataclass(i)

    @classmethod
    def add_one(cls, playlist: dict[str, Any]):
        playlist["userid"] = get_current_userid()
        result = cls.insert_one(playlist)

        return result.lastrowid

    @classmethod
    def check_exists_by_name(cls, name: str):
        result = cls.execute(
            select(cls).where((cls.name == name) & (cls.userid == get_current_userid()))
        )
        return next(result).scalar() is not None

    @classmethod
    def append_to_playlist(cls, id: int, trackhashes: list[str]):
        dbtrackhashes = cls.get_trackhashes(id)
        if not dbtrackhashes:
            dbtrackhashes = []

        return next(
            cls.execute(
                update(cls)
                .where((cls.id == id) & (cls.userid == get_current_userid()))
                .values(trackhashes=dbtrackhashes + trackhashes),
                commit=True,
            )
        )

    @classmethod
    def get_trackhashes(cls, id: int):
        result = cls.execute(
            select(cls.trackhashes).where(
                (cls.id == id) & (cls.userid == get_current_userid())
            )
        )
        return next(result).scalar()

    @classmethod
    def remove_from_playlist(cls, id: int, trackhashes: list[dict[str, Any]]):
        # INFO: Get db trackhashes
        dbtrackhashes = cls.get_trackhashes(id)
        if dbtrackhashes:
            for item in trackhashes:
                if dbtrackhashes.index(item["trackhash"]) == item["index"]:
                    dbtrackhashes.remove(item["trackhash"])

            return next(
                cls.execute(
                    update(cls)
                    .where((cls.id == id) & (cls.userid == get_current_userid()))
                    .values(trackhashes=dbtrackhashes),
                    commit=True,
                )
            )

    @classmethod
    def get_by_id(cls, id: int):
        result = cls.execute(
            select(cls).where((cls.id == id) & (cls.userid == get_current_userid()))
        )
        result = next(result).scalar()

        if result:
            return playlist_to_dataclass(result)

    @classmethod
    def update_one(cls, id: int, playlist: dict[str, Any]):
        return next(
            cls.execute(
                update(cls)
                .where((cls.id == id) & (cls.userid == get_current_userid()))
                .values(playlist),
                commit=True,
            )
        )

    @classmethod
    def update_settings(cls, id: int, settings: dict[str, Any]):
        return next(
            cls.execute(
                update(cls)
                .where((cls.id == id) & (cls.userid == get_current_userid()))
                .values(settings=settings),
                commit=True,
            )
        )

    @classmethod
    def remove_image(cls, id: int):
        return next(
            cls.execute(
                update(cls)
                .where((cls.id == id) & (cls.userid == get_current_userid()))
                .values(image=None),
                commit=True,
            )
        )


class LibDataTable(Base):
    __tablename__ = "artistdata"

    id: Mapped[int] = mapped_column(primary_key=True)
    itemhash: Mapped[str] = mapped_column(String(), unique=True, index=True)
    itemtype: Mapped[str] = mapped_column(String())
    color: Mapped[str] = mapped_column(String(), nullable=True)
    bio: Mapped[str] = mapped_column(String(), nullable=True)
    info: Mapped[dict[str, Any]] = mapped_column(JSON(), nullable=True)
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def update_one(cls, hash: str, data: dict[str, Any]):
        return next(
            cls.execute(
                update(cls).where(cls.itemhash == hash).values(data), commit=True
            )
        )

    @classmethod
    def find_one(cls, hash: str, type: Literal["album", "artist"]):
        result = cls.execute(
            select(cls).where((cls.itemhash == type + hash) & (cls.itemtype == type))
        )
        return next(result).scalar()

    @classmethod
    def get_all_colors(cls, type: str) -> Iterable[dict[str, str]]:
        result = cls.execute(select(cls).where(cls.itemtype == type))

        for i in next(result).scalars():
            yield {"itemhash": i.itemhash.replace(type, ""), "color": i.color}


class MixTable(Base):
    __tablename__ = "mix"

    id: Mapped[int] = mapped_column(primary_key=True)
    mixid: Mapped[str] = mapped_column(String(), index=True)
    title: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    timestamp: Mapped[int] = mapped_column(Integer())
    sourcehash: Mapped[str] = mapped_column(String(), unique=True, index=True)
    userid: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade"), index=True
    )
    saved: Mapped[bool] = mapped_column(Boolean(), default=False)
    tracks: Mapped[list[str]] = mapped_column(JSON(), default_factory=list)
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def get_all(cls, with_userid: bool = False):
        if with_userid:
            result = cls.execute(
                select(cls)
                .where(cls.userid == get_current_userid())
                .order_by(cls.timestamp.desc())
            )
        else:
            result = cls.execute(select(cls).order_by(cls.timestamp.desc()))

        for i in next(result).scalars():
            yield Mix.mix_to_dataclass(i)

    @classmethod
    def get_by_sourcehash(cls, sourcehash: str):
        result = cls.execute(select(cls).where(cls.sourcehash == sourcehash))

        res = next(result).scalar()

        if res:
            return Mix.mix_to_dataclass(res)

    @classmethod
    def get_by_mixid(cls, mixid: str):
        result = cls.execute(select(cls).where(cls.mixid == mixid))
        res = next(result).scalar()

        if res:
            return Mix.mix_to_dataclass(res)

    @classmethod
    def insert_one(cls, mix: Mix):
        mixdict = asdict(mix)
        mixdict["mixid"] = mix.id
        del mixdict["id"]

        return next(cls.execute(insert(cls).values(mixdict), commit=True))

    @classmethod
    def update_one(cls, mixid: str, mix: Mix):
        mixdict = asdict(mix)
        mixdict["mixid"] = mix.id
        del mixdict["id"]

        return next(
            cls.execute(
                update(cls)
                .where(
                    and_(
                        cls.mixid == mixid,
                        cls.sourcehash == mix.sourcehash,
                        cls.userid == get_current_userid(),
                    )
                )
                .values(mixdict),
                commit=True,
            )
        )

    @classmethod
    def save_artist_mix(cls, sourcehash: str):
        """
        Toggles the saved status of an artist mix.
        """

        mix = cls.get_by_sourcehash(sourcehash)

        if not mix:
            return False

        mix.saved = not mix.saved
        cls.update_one(mix.id, mix)

        return mix.saved

    @classmethod
    def get_saved_track_mixes(cls):
        """
        Return all mixes that have the extra.trackmix_saved set to True.
        """

        result = cls.execute(select(cls).where(cls.extra.c.trackmix_saved == True))
        # return Mix.mixes_to_dataclasses(result.fetchall())

        for i in next(result).scalars():
            yield Mix.mix_to_dataclass(i)

    @classmethod
    def save_track_mix(cls, sourcehash: str):
        """
        Toggles the property extra.trackmix_saved to True.
        """

        mix = cls.get_by_sourcehash(sourcehash)
        if not mix:
            return False

        mix.extra["trackmix_saved"] = not mix.extra.get("trackmix_saved", False)
        cls.update_one(mix.id, mix)

        return mix.extra["trackmix_saved"]


class CollectionTable(Base):
    # INFO: table name was kept as page to avoid breaking existing data
    __tablename__ = "page"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(), index=True)
    userid: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade"), index=True
    )
    items: Mapped[list[dict[str, Any]]] = mapped_column(JSON(), default_factory=list)
    extra: Mapped[dict[str, Any]] = mapped_column(
        JSON(), nullable=True, default_factory=dict
    )

    @classmethod
    def to_dict(cls, entry: Any) -> dict[str, Any]:
        d = entry.__dict__
        del d["_sa_instance_state"]
        return d

    @classmethod
    def get_all(cls):
        result = cls.execute(select(cls).where(cls.userid == get_current_userid()))

        for i in next(result).scalars():
            yield cls.to_dict(i)

    @classmethod
    def get_by_id(cls, id: int):
        result = cls.execute(
            select(cls).where(and_(cls.id == id, cls.userid == get_current_userid()))
        )
        res = next(result).scalar()

        if res:
            return cls.to_dict(res)

    @classmethod
    def delete_by_id(cls, id: int):
        return next(
            cls.execute(
                delete(cls).where(
                    and_(cls.id == id, cls.userid == get_current_userid())
                ),
                commit=True,
            )
        )

    @classmethod
    def update_items(cls, id: int, items: list[dict[str, Any]]):
        return next(
            cls.execute(
                update(cls)
                .where(and_(cls.id == id, cls.userid == get_current_userid()))
                .values(items=items),
                commit=True,
            )
        )

    @classmethod
    def update_one(cls, payload: dict[str, Any]):
        return next(
            cls.execute(
                update(cls)
                .where(
                    and_(cls.id == payload["id"], cls.userid == get_current_userid())
                )
                .values(payload),
                commit=True,
            )
        )
