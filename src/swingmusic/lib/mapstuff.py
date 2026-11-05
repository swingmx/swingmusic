from swingmusic.db.userdata import LibDataTable, FavoritesTable, ScrobbleTable
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.folder import FolderStore
from swingmusic.store.plays import PlayStore, split_playcount
from swingmusic.store.tracks import TrackStore




def map_trackhash_repairs():
    """
    Repairs trackhash-keyed user data (scrobbles and track favorites) whose
    trackhash no longer resolves — eg. after files were retagged or the
    hashing inputs changed.
    """
    basename_index: dict[str, list[str]] | None = None

    def resolve(filepath: str | None) -> str | None:
        nonlocal basename_index

        if not filepath:
            return None

        trackhash = FolderStore.map.get(filepath)
        if trackhash is not None:
            return trackhash

        if basename_index is None:
            basename_index = {}
            for path in FolderStore.map:
                basename_index.setdefault(path.rsplit("/", 1)[-1], []).append(path)

        candidates = basename_index.get(filepath.rsplit("/", 1)[-1], [])
        if len(candidates) == 1:
            return FolderStore.map.get(candidates[0])

        # ambiguous or missing — leave the entry alone
        return None

    # distinct orphaned trackhash -> stored filepath
    orphans: dict[str, str | None] = {}
    for record in ScrobbleTable.get_all_unfiltered():
        if record.trackhash not in TrackStore.trackhashmap:
            orphans.setdefault(record.trackhash, (record.extra or {}).get("filepath"))

    repaired = 0
    for old, filepath in orphans.items():
        new = resolve(filepath)
        if new is not None:
            ScrobbleTable.update_trackhash(old, new)
            repaired += 1

    fav_orphans: dict[str, str | None] = {}
    for entry in FavoritesTable.get_all():
        if entry.type != "track":
            continue
        if entry.hash not in TrackStore.trackhashmap:
            fav_orphans.setdefault(entry.hash, (entry.extra or {}).get("filepath"))

    for old, filepath in fav_orphans.items():
        new = resolve(filepath)
        if new is not None:
            FavoritesTable.update_track_hash(old, new)
            repaired += 1

    if repaired:
        print(f"Repaired {repaired} user data trackhashes")


def map_scrobble_data():
    """
    Maps every user's scrobbles to their play stats for tracks, albums and artists.
    """
    PlayStore.clear()

    for record in ScrobbleTable.get_all_unfiltered():
        group = TrackStore.trackhashmap.get(record.trackhash)

        if group is None:
            continue

        track = group.tracks[0]
        PlayStore.record(
            record.userid,
            record.trackhash,
            track.albumhash,
            track.artisthashes,
            record.duration,
            record.timestamp,
            split_playcount(record.duration, track.duration),
        )


def map_favorites():
    """
    Maps favorites data to the in-memory stores.
    """
    favorites = FavoritesTable.get_all()

    for entry in favorites:
        if entry.type == "album":
            album = AlbumStore.albummap.get(entry.hash)
            if album:
                album.toggle_favorite_user(entry.userid)

        elif entry.type == "artist":
            artist = ArtistStore.artistmap.get(entry.hash)
            if artist:
                artist.toggle_favorite_user(entry.userid)

        elif entry.type == "track":
            track = TrackStore.trackhashmap.get(entry.hash)
            if track:
                track.toggle_favorite_user(entry.userid)


def map_artist_colors():
    colors = LibDataTable.get_all_colors(type="artist")

    for color in colors:
        artist = ArtistStore.artistmap.get(color["itemhash"])

        if artist:
            blurhash: str = (color.get("extra", {}) or {}).get("blurhash", "")
            artist.update_color_info(color["color"], blurhash)


def map_album_colors():
    colors = LibDataTable.get_all_colors(type="album")

    for color in colors:
        album = AlbumStore.albummap.get(color["itemhash"])

        if not album:
            continue

        blurhash: str = (color.get("extra", {}) or {}).get("blurhash", "")
        album.update_color_info(color["color"], blurhash)

        for trackhash in album.trackhashes:
            group = TrackStore.trackhashmap.get(trackhash)

            if not group:
                continue

            group.update_color_info(color["color"], blurhash)
