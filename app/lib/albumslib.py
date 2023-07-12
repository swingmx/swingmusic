"""
Contains methods relating to albums.
"""

from tqdm import tqdm
from app.store.albums import AlbumStore
from app.store.tracks import TrackStore


def validate_albums():
    """
    Removes albums that have no tracks.

    Probably albums that were added from incompletely written files.
    """

    album_hashes = {t.albumhash for t in TrackStore.tracks}
    albums = AlbumStore.albums

    for album in tqdm(albums, desc="Validating albums"):
        if album.albumhash not in album_hashes:
            AlbumStore.remove_album(album)
