"""
Re-keys user data when the track or album hash of a file changes between loads.
"""

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from swingmusic.db.engine import DbEngine
from swingmusic.db.userdata import (
    CollectionTable,
    FavoritesTable,
    HashSnapshotTable,
    MixTable,
    PlaylistTable,
    ScrobbleTable,
)
from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore


def current_hashes() -> dict[str, tuple[str, str]]:
    """
    Returns {filepath: (trackhash, albumhash)} for every loaded track.
    """
    return {
        track.filepath: (track.trackhash, track.albumhash)
        for group in TrackStore.trackhashmap.values()
        for track in group.tracks
    }


def hash_changes(
    snapshot: dict[str, tuple[str, str]], current: dict[str, tuple[str, str]]
) -> tuple[dict[str, str], dict[str, str]]:
    """
    Returns the old -> new track and album hashes of files present in both,
    skipping old hashes that still exist in the library.
    """
    tracks: dict[str, str] = {}
    albums: dict[str, str] = {}

    for filepath, (trackhash, albumhash) in current.items():
        old = snapshot.get(filepath)
        if old is None:
            continue

        if old[0] != trackhash and old[0] not in TrackStore.trackhashmap:
            tracks.setdefault(old[0], trackhash)

        if old[1] != albumhash and old[1] not in AlbumStore.albummap:
            albums.setdefault(old[1], albumhash)

    return tracks, albums


def remap(hashes: list[str], mapping: dict[str, str]) -> list[str]:
    """
    Returns `hashes` with mapped entries replaced and duplicates removed.
    """
    return list(dict.fromkeys(mapping.get(h, h) for h in hashes))


def migrate_favorites(session: Session, tracks: dict[str, str], albums: dict[str, str]):
    """
    Re-keys track and album favorites, dropping those whose new key is already a favorite.
    """
    for itemtype, mapping in (("track", tracks), ("album", albums)):
        keys = {f"{itemtype}_{old}": new for old, new in mapping.items()}
        keys.update({old: new for old, new in mapping.items()})

        rows = session.scalars(
            select(FavoritesTable).where(
                FavoritesTable.type == itemtype, FavoritesTable.hash.in_(keys)
            )
        ).all()

        for row in rows:
            newkey = f"{itemtype}_{keys[row.hash]}"
            exists = session.scalar(
                select(FavoritesTable.id).where(FavoritesTable.hash == newkey)
            )

            if exists is None:
                row.hash = newkey
            else:
                session.delete(row)

            session.flush()


def migrate_scrobbles(session: Session, tracks: dict[str, str], albums: dict[str, str]):
    """
    Re-keys scrobbled tracks and album and track play sources.
    """
    for old, new in tracks.items():
        session.execute(
            update(ScrobbleTable).where(ScrobbleTable.trackhash == old).values(trackhash=new)
        )

    sources = {f"tr:{old}": f"tr:{new}" for old, new in tracks.items()}
    sources.update({f"al:{old}": f"al:{new}" for old, new in albums.items()})

    for old, new in sources.items():
        session.execute(
            update(ScrobbleTable).where(ScrobbleTable.source == old).values(source=new)
        )


def migrate_lists(session: Session, tracks: dict[str, str], albums: dict[str, str]):
    """
    Re-keys the hashes stored in playlists, mixes and collections.
    """
    for playlist in session.scalars(select(PlaylistTable)):
        trackhashes = remap(playlist.trackhashes or [], tracks)
        if trackhashes != playlist.trackhashes:
            playlist.trackhashes = trackhashes

    for mix in session.scalars(select(MixTable)):
        trackhashes = remap(mix.tracks or [], tracks)
        if trackhashes != mix.tracks:
            mix.tracks = trackhashes

        extra = dict(mix.extra or {})
        for key, mapping in (("sourcetracks", tracks), ("albums", albums)):
            if isinstance(extra.get(key), list):
                extra[key] = remap(extra[key], mapping)

        if extra != (mix.extra or {}):
            mix.extra = extra

    mappings = {"track": tracks, "album": albums}
    for collection in session.scalars(select(CollectionTable)):
        items = [
            {**item, "hash": mappings[item["type"]].get(item["hash"], item["hash"])}
            if item.get("type") in mappings and "hash" in item
            else item
            for item in collection.items or []
        ]

        if items != collection.items:
            collection.items = items


def migrate_user_data(tracks: dict[str, str], albums: dict[str, str]):
    """
    Re-keys all user data from old to new track and album hashes in one transaction.
    """
    with DbEngine.manager(commit=True) as session:
        migrate_favorites(session, tracks, albums)
        migrate_scrobbles(session, tracks, albums)
        migrate_lists(session, tracks, albums)


def map_hash_migrations():
    """
    Moves user data to the current hashes of files whose hashes changed
    since the last load, then saves the current hashes.
    """
    snapshot = HashSnapshotTable.get_all()
    current = current_hashes()
    tracks, albums = hash_changes(snapshot, current)

    if tracks or albums:
        migrate_user_data(tracks, albums)
        print(f"Migrated user data for {len(tracks)} track and {len(albums)} album hashes")

    changed = {f: h for f, h in current.items() if snapshot.get(f) != h}
    removed = snapshot.keys() - current.keys()

    if changed or removed:
        HashSnapshotTable.apply(changed, removed)
