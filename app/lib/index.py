import gc
from time import time
from app.lib.mapstuff import (
    map_album_colors,
    map_artist_colors,
    map_favorites,
    map_scrobble_data,
)
from app.lib.populate import CordinateMedia
from app.lib.tagger import IndexTracks
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.folder import FolderStore
from app.store.tracks import TrackStore
from app.utils.threading import background


class IndexEverything:
    def __init__(self) -> None:
        IndexTracks(instance_key=time())

        key = str(time())
        TrackStore.load_all_tracks(key)
        AlbumStore.load_albums(key)
        ArtistStore.load_artists(key)
        FolderStore.load_filepaths()

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
