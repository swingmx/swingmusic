from app.lib.mapstuff import map_favorites, map_scrobble_data
from app.lib.populate import CordinateMedia
from app.lib.tagger import IndexTracks
from app.store.folder import FolderStore


import gc
from time import time

from app.utils.threading import background


class IndexEverything:
    def __init__(self) -> None:
        IndexTracks(instance_key=time())
        FolderStore.load_filepaths()
        map_scrobble_data()
        map_favorites()
        # CordinateMedia(instance_key=str(time()))
        gc.collect()


@background
def index_everything():
    return IndexEverything()
