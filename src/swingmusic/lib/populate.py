import os
from dataclasses import asdict
from typing import Generator
from requests import ReadTimeout
from concurrent.futures import ProcessPoolExecutor
from requests import ConnectionError as RequestConnectionError
import logging

from swingmusic import settings
from swingmusic.lib.artistlib import CheckArtistImages
from swingmusic.lib.taglib import extract_thumb
from swingmusic.models import Album, Artist
from swingmusic.models.lastfm import SimilarArtist
from swingmusic.models.track import Track
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.utils.network import has_connection
from swingmusic.utils.progressbar import tqdm
from swingmusic.requests.artists import fetch_similar_artists
from swingmusic.lib.colorlib import ProcessAlbumColors, ProcessArtistColors

from swingmusic.db.userdata import SimilarArtistTable

log = logging.getLogger(__name__)


class CordinateMedia:
    """
    Cordinates the extracting of thumbnails
    """

    def __init__(self, instance_key: str):
        ProcessTrackThumbnails()
        ProcessAlbumColors()
        ProcessArtistColors()

        tried_to_download_new_images = False

        if has_connection():
            tried_to_download_new_images = True
            try:
                CheckArtistImages()
            except (RequestConnectionError, ReadTimeout) as e:
                log.error(
                    "Internet connection lost. Downloading artist images suspended."
                )
                log.error(e)  # REVIEW More informations = good
        else:
            log.warning("No internet connection. Downloading artist images suspended!")

        # Re-process the new artist images.
        if tried_to_download_new_images:
            ProcessArtistColors()

        if has_connection():
            print("Attempting to download similar artists...")
            FetchSimilarArtistsLastFM()


def get_image(tracks: list[Track], paths=None):
    """
    The function retrieves an image from a list of tracks by extracting the thumbnail from the first track that has one.

    :param tracks: A list of Track objects to extract the image from.
    :type tracks: list[Track]
    :return: None
    """

    for track in tracks:
        extracted = extract_thumb(track.filepath, track.albumhash + ".webp", paths)

        if extracted:
            return


class ProcessTrackThumbnails:
    """
    Extracts the album art from all albums in album store.
    """

    def extract(self, albums: list[Album]):
        """
        Extracts the album art with platform-specific logic.
        """

        cpus = max(1, os.cpu_count() // 2)

        albumsMap = ( AlbumStore.get_album_tracks(album.albumhash) for album in albums )

        # Create process pool with worker function
        with Pool(processes=cpus) as pool:
            worker = partial(get_image, paths=settings.Paths())
            # Process files and track progress

            results = list(
                tqdm(
                    pool.imap_unordered(worker, albumsMap),
                    total=len(albums),
                    desc="Extracting track images",
                )
            )

            list(results)

    def __init__(self) -> None:
        """
        Filters out albums that already have thumbnails and
        extracts the thumbnail for the other albums.
        """
        path = settings.Paths().sm_thumb_path

        # read all the files in the thumbnail directory
        processed = set(i.replace(".webp", "") for i in os.listdir(path))
        # filter out albums that already have thumbnails
        albums = filter(
            lambda album: album.albumhash not in processed,
            AlbumStore.get_flat_list(),
        )

        albums = list(albums)
        self.extract(albums)


def save_similar_artists(artist: Artist):
    """
    Downloads and saves similar artists to the database.
    """
    if SimilarArtistTable.exists(artist.artisthash):
        return

    artists = fetch_similar_artists(artist.name)

    # INFO: Nones mean there was a connection error
    if artists is None:
        return

    artist_ = SimilarArtist(artist.artisthash, artists)
    SimilarArtistTable.insert_one(asdict(artist_))


class FetchSimilarArtistsLastFM:
    """
    Fetches similar artists from LastFM using a thread pool.
    """

    def __init__(self) -> None:
        # read all artists from db
        storeArtists = ArtistStore.get_flat_list()
        processed = set(a.artisthash for a in SimilarArtistTable.get_all())

        # filter out artists that already have similar artists using generator
        artists = (
            artist for artist in storeArtists if artist.artisthash not in processed
        )

        cpus = max(1, (os.cpu_count() or 1) // 2)

        with ProcessPoolExecutor(max_workers=cpus) as executor:
            try:
                # negative total length
                results = list(
                    tqdm(
                        executor.map(save_similar_artists, artists),
                        total=len(storeArtists) - len(processed),
                        desc="Fetching similar artists",
                    )
                )

                list(results)
            # any exception that can be raised by the pool
            except Exception as e:
                log.warning(e)
                return
