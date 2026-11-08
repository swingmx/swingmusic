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
    false,
    func,
    insert,
    or_,
    select,
    update,
)

from sqlalchemy.dialects.sqlite import insert as sqlite_insert
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
from swingmusic.utils.dates import create_new_date


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
    def update_track_hash(cls, old: str, new: str):
        """
        Re-keys a track favorite whose trackhash changed. Matches both the
        prefixed and legacy unprefixed hash forms.
        """
        return next(
            cls.execute(
                update(cls)
                .where(cls.hash.in_((f"track_{old}", old)))
                .values(hash=f"track_{new}"),
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
    def get_all_unfiltered(cls):
        """
        All scrobbles for ALL users (the trackhash repair pass runs at
        boot, outside any request context).
        """
        result = cls.execute(select(cls).execution_options(yield_per=100))

        for i in next(result).scalars():
            yield tracklog_to_dataclass(i)

    @classmethod
    def update_trackhash(cls, old: str, new: str):
        """
        Re-keys all scrobbles of a track whose trackhash changed.
        """
        return next(
            cls.execute(
                update(cls).where(cls.trackhash == old).values(trackhash=new),
                commit=True,
            )
        )

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
    def get_by_name(cls, name: str):
        result = cls.execute(
            select(cls).where((cls.name == name) & (cls.userid == get_current_userid()))
        )
        return next(result).scalar()

    @classmethod
    def append_to_playlist(cls, id: int, trackhashes: list[str]):
        dbtrackhashes = cls.get_trackhashes(id) or []
        # Preserve order: start with existing hashes, then add new ones that aren't already present
        seen = set(dbtrackhashes)
        added = [h for h in dict.fromkeys(trackhashes) if h not in seen]

        if not added:
            return

        return next(
            cls.execute(
                update(cls)
                .where((cls.id == id) & (cls.userid == get_current_userid()))
                .values(trackhashes=dbtrackhashes + added, last_updated=create_new_date()),
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
            removed = False
            for item in trackhashes:
                if dbtrackhashes.index(item["trackhash"]) == item["index"]:
                    dbtrackhashes.remove(item["trackhash"])
                    removed = True

            if not removed:
                return

            return next(
                cls.execute(
                    update(cls)
                    .where((cls.id == id) & (cls.userid == get_current_userid()))
                    .values(trackhashes=dbtrackhashes, last_updated=create_new_date()),
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


class HashSnapshotTable(Base):
    """
    The track and album hashes each file had when the library was last loaded.
    """

    __tablename__ = "hashsnapshot"

    filepath: Mapped[str] = mapped_column(String(), primary_key=True)
    trackhash: Mapped[str] = mapped_column(String())
    albumhash: Mapped[str] = mapped_column(String())

    @classmethod
    def get_all(cls) -> dict[str, tuple[str, str]]:
        """
        Returns the snapshot as {filepath: (trackhash, albumhash)}.
        """
        result = next(cls.execute(select(cls.filepath, cls.trackhash, cls.albumhash)))
        return {filepath: (trackhash, albumhash) for filepath, trackhash, albumhash in result}

    @classmethod
    def apply(cls, changed: dict[str, tuple[str, str]], removed: Iterable[str]):
        """
        Upserts the changed filepaths and deletes the removed ones.
        """
        removed = list(removed)

        with DbEngine.manager(commit=True) as session:
            for start in range(0, len(removed), 500):
                session.execute(delete(cls).where(cls.filepath.in_(removed[start : start + 500])))

            if changed:
                stmt = sqlite_insert(cls)
                session.execute(
                    stmt.on_conflict_do_update(
                        index_elements=[cls.filepath],
                        set_={"trackhash": stmt.excluded.trackhash, "albumhash": stmt.excluded.albumhash},
                    ),
                    [
                        {"filepath": f, "trackhash": t, "albumhash": a}
                        for f, (t, a) in changed.items()
                    ],
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

        item = next(result).scalar()
        if item:
            return {
                "itemhash": item.itemhash.replace(type, ""),
                "type": type,
                "color": item.color,
                "extra": item.extra,
            }

        return None

    @classmethod
    def get_all_colors(cls, type: str) -> Iterable[dict[str, str]]:
        result = cls.execute(select(cls).where(cls.itemtype == type))

        for i in next(result).scalars():
            yield {
                "itemhash": i.itemhash.replace(type, ""),
                "type": type,
                "color": i.color,
                "extra": i.extra,
            }


class ClassicalCacheTable(Base):
    __tablename__ = "classicalcache"

    id: Mapped[int] = mapped_column(primary_key=True)
    albumhash: Mapped[str] = mapped_column(String(), unique=True, index=True)
    contenthash: Mapped[str] = mapped_column(String())
    # kept in the column that used to hold the parser version
    result_hash: Mapped[str] = mapped_column("parser_version", String())
    result: Mapped[dict[str, Any]] = mapped_column(JSON())

    @classmethod
    def get_all(cls) -> dict[str, dict[str, Any]]:
        """
        Cached parse results keyed by albumhash.
        """
        rows = {}
        result = cls.execute(select(cls))
        for row in next(result).scalars():
            rows[row.albumhash] = {
                "contenthash": row.contenthash,
                "result_hash": row.result_hash,
                "result": row.result,
            }
        return rows

    @classmethod
    def replace_many(cls, rows: list[dict[str, Any]]):
        """
        Replace the cached rows for the given albums.
        """
        if not rows:
            return
        hashes = [row["albumhash"] for row in rows]
        next(cls.execute(delete(cls).where(cls.albumhash.in_(hashes)), commit=True))
        cls.insert_many(rows)


class ClassicalEntityTable(Base):
    __tablename__ = "classicalentity"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(), index=True)
    remote_id: Mapped[str] = mapped_column(String(), index=True)
    hash: Mapped[str] = mapped_column(String())
    status: Mapped[str] = mapped_column(String())
    data: Mapped[dict[str, Any]] = mapped_column(JSON())
    updated_at: Mapped[int] = mapped_column(Integer())

    @classmethod
    def get_all(cls) -> dict[tuple[str, str], dict[str, Any]]:
        """
        Enriched records keyed by (kind, remote_id).
        """
        rows = {}
        result = cls.execute(select(cls))
        for row in next(result).scalars():
            rows[(row.kind, row.remote_id)] = {
                "hash": row.hash,
                "status": row.status,
                "data": row.data,
                "updated_at": row.updated_at,
            }
        return rows

    @classmethod
    def replace_many(cls, rows: list[dict[str, Any]]):
        """
        Replace the rows for the given (kind, remote_id) pairs.
        """
        if not rows:
            return
        for row in rows:
            next(
                cls.execute(
                    delete(cls).where(
                        and_(cls.kind == row["kind"], cls.remote_id == row["remote_id"])
                    ),
                    commit=True,
                )
            )
        cls.insert_many(rows)

    @classmethod
    def remove_many(cls, keys: list[tuple[str, str]]):
        for kind, remote_id in keys:
            next(
                cls.execute(
                    delete(cls).where(and_(cls.kind == kind, cls.remote_id == remote_id)),
                    commit=True,
                )
            )


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
    def trackmix_saved(cls):
        """
        SQL expression for whether a row's track mix is saved, as 0 or 1.
        """
        return func.coalesce(func.json_extract(cls.extra, "$.trackmix_saved"), 0)

    @classmethod
    def count_saved(cls, min_trackmix_tracks: int | None) -> int:
        """
        Counts the current user's saved artist mixes and saved track mixes.
        Track mixes count when their artist mix has more than `min_trackmix_tracks` tracks; None skips them.
        """
        trackmixes = false()
        if min_trackmix_tracks is not None:
            trackmixes = and_(
                cls.trackmix_saved() == 1,
                func.json_array_length(cls.tracks) > min_trackmix_tracks,
            )

        result = cls.execute(
            select(
                func.count().filter(cls.saved.is_(True)),
                func.count().filter(trackmixes),
            ).where(cls.userid == get_current_userid())
        )

        return sum(next(result).one())

    @classmethod
    def get_saved(cls) -> list[Mix]:
        """
        Returns the current user's mixes whose artist mix or track mix is saved, newest first.
        """
        result = cls.execute(
            select(cls)
            .where(
                cls.userid == get_current_userid(),
                or_(cls.saved.is_(True), cls.trackmix_saved() == 1),
            )
            .order_by(cls.timestamp.desc(), cls.id.desc())
        )

        return [Mix.mix_to_dataclass(i) for i in next(result).scalars()]

    @classmethod
    def get_page(cls, ids: Any, start: int, limit: int) -> tuple[list[Mix], int]:
        """
        Returns the mixes with ids in the `ids` subquery from `start`, newest first, and their total.
        """
        total = cls.execute(select(func.count()).select_from(ids.subquery()))
        total = next(total).scalar_one()

        result = cls.execute(
            select(cls)
            .where(cls.id.in_(ids))
            .order_by(cls.timestamp.desc(), cls.id.desc())
            .offset(start)
            .limit(limit)
        )

        return [Mix.mix_to_dataclass(i) for i in next(result).scalars()], total

    @classmethod
    def get_unsaved_artist_mixes(cls, start: int, limit: int) -> tuple[list[Mix], int]:
        """
        Returns a page of the current user's unsaved artist mixes and their total.
        """
        ids = select(cls.id).where(
            cls.userid == get_current_userid(), cls.saved.is_not(True)
        )
        return cls.get_page(ids, start, limit)

    @classmethod
    def get_unsaved_trackmix_sources(
        cls, min_tracks: int, start: int, limit: int
    ) -> tuple[list[Mix], int]:
        """
        Returns a page of the newest mix per artist with more than `min_tracks` tracks,
        skipping artists with a saved track mix, and their total.
        """
        artisthash = func.json_extract(cls.extra, "$.artisthash")
        ranked = (
            select(
                cls.id,
                func.row_number()
                .over(
                    partition_by=artisthash,
                    order_by=(cls.timestamp.desc(), cls.id.desc()),
                )
                .label("rank"),
                func.max(cls.trackmix_saved())
                .over(partition_by=artisthash)
                .label("anysaved"),
            )
            .where(
                cls.userid == get_current_userid(),
                func.json_array_length(cls.tracks) > min_tracks,
            )
            .subquery()
        )

        ids = select(ranked.c.id).where(ranked.c.rank == 1, ranked.c.anysaved == 0)
        return cls.get_page(ids, start, limit)

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
