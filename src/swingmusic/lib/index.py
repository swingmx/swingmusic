import gc
import logging
from time import time

from swingmusic.config import UserConfig
from swingmusic.db.libdata import TrackTable
from swingmusic.lib.tagger import IndexTracks, resolve_root_dirs, root_prefixes
from swingmusic.lib.populate import CordinateMedia, CordinateOnlineMedia
from swingmusic.lib.recipes.recents import RecentlyAdded

from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore
from swingmusic.store.folder import FolderStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.general import GeneralStore

from swingmusic.lib.hashmigration import map_hash_migrations
from swingmusic.lib.mapstuff import (
    map_favorites,
    map_album_colors,
    map_scrobble_data,
    map_artist_colors,
    map_trackhash_repairs,
)
from swingmusic.premium import ClassicalStore, LicenseError
from swingmusic.utils.threading import background

log = logging.getLogger(__name__)


def prune_outside_roots() -> int:
    """
    Delete tracks whose files are outside the configured root directories.
    Returns the number of rows removed.
    """
    roots = resolve_root_dirs(UserConfig().rootDirs)
    if not roots:
        return 0

    prefixes = root_prefixes(roots)
    stale = {
        filepath
        for filepath in TrackTable.get_all_filepaths()
        if not filepath.startswith(prefixes)
    }
    if stale:
        TrackTable.remove_tracks_by_filepaths(stale)
        log.info(f"Removed {len(stale)} tracks outside the root directories")
    return len(stale)


def prepare_full_scan():
    """
    Prepares the server state for a full scan.

    Drops the tracks db table.
    Resets in-memory stores.
    Does NOT remove scrobbles, favorites, playlists, collections, and other user data.
    """

    TrackTable.reset()
    TrackStore.reset()
    ArtistStore.reset()
    AlbumStore.reset()
    FolderStore.reset()

    GeneralStore.start_full_scan()


@background
def index_everything(full_scan: bool = False):
    """
    Indexes everything.

    :param full_scan: Whether to perform a full scan of the root directories.
    """

    if full_scan:
        prepare_full_scan()

    IndexTracks()

    key = str(time())
    TrackStore.load_all_tracks(key)
    AlbumStore.load_albums(key)
    ArtistStore.load_artists(key)
    FolderStore.load_filepaths()

    # NOTE: Rebuild recently added items on the homepage store
    RecentlyAdded()

    # map colors
    map_album_colors()
    map_artist_colors()

    # INFO: Re-key user data of changed hashes before mapping it
    map_hash_migrations()
    map_trackhash_repairs()

    map_scrobble_data()
    map_favorites()

    if ClassicalStore is not None:
        try:
            ClassicalStore.load_albums(key)
        except LicenseError:
            pass

    CordinateMedia(instance_key=str(time()), overwrite_track_thumbnails=full_scan)
    GeneralStore.end_full_scan()
    log.info("Indexing completed")

    CordinateOnlineMedia()
    gc.collect()
