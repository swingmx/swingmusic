"""
Contains methods relating to albums.
"""

from alive_progress import alive_bar

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.logger import log


def validate_albums():
    """
    Removes albums that have no tracks.

    Probably albums that were added from incompletely written files.
    """

    album_hashes = {t.albumhash for t in TrackStore.tracks}
    albums = AlbumStore.albums

    with alive_bar(len(albums)) as bar:
        log.info("Validating albums")
        for album in albums:
            if album.albumhash not in album_hashes:
                AlbumStore.remove_album(album)
            bar()
