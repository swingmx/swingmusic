import gc
from time import time
from swingmusic.lib.mapstuff import (
    map_album_colors,
    map_artist_colors,
    map_favorites,
    map_scrobble_data,
)
from swingmusic.lib.populate import CordinateMedia
from swingmusic.lib.recipes.recents import RecentlyAdded
from swingmusic.lib.tagger import IndexTracks
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.folder import FolderStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.threading import background


class IndexEverything:
    def __init__(self) -> None:
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

        map_scrobble_data()
        map_favorites()

        CordinateMedia(instance_key=str(time()))
        gc.collect()


@background
def index_everything():
    return IndexEverything()
