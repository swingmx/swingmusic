from dataclasses import asdict
import os
from concurrent.futures import ProcessPoolExecutor
import platform

from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from swingmusic import settings
from swingmusic.lib.artistlib import CheckArtistImages
from swingmusic.lib.colorlib import ProcessAlbumColors, ProcessArtistColors
from swingmusic.lib.taglib import extract_thumb
from swingmusic.logger import log
from swingmusic.models import Album, Artist
from swingmusic.models.lastfm import SimilarArtist
from swingmusic.requests.artists import fetch_similar_artists
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.utils.network import has_connection
from swingmusic.utils.progressbar import tqdm

from swingmusic.db.userdata import SimilarArtistTable


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


def get_image(album: Album):
    """
    The function retrieves an image from an album by iterating through its tracks and extracting the thumbnail from the first track that has one.

    :param album: An instance of the `Album` class representing the album to retrieve the image from.
    :type album: Album
    :return: None
    """
    matching_tracks = AlbumStore.get_album_tracks(album.albumhash)

    for track in matching_tracks:
        extracted = extract_thumb(track.filepath, track.albumhash + ".webp")

        if extracted:
            return


class ProcessTrackThumbnails:
    """
    Extracts the album art from all albums in album store.
    """

    def extract(self, albums: list[Album]):
        """
        Extracts the album art with platform specific logic.
        """

        if platform.system() == "Linux":
            # INFO: Processess are forked with access to global stores
            # It's "safe" to use a process pool
            cpus = max(1, os.cpu_count() // 2)
            with ProcessPoolExecutor(max_workers=cpus) as executor:
                results = list(
                    tqdm(
                        executor.map(get_image, albums),
                        total=len(albums),
                        desc="Extracting track images",
                    )
                )

                list(results)
        else:
            # INFO: Use a for loop for windows (and others I guess)
            for album in tqdm(albums, desc="Extracting track images"):
                get_image(album)

    def __init__(self) -> None:
        """
        Filters out albums that already have thumbnails and
        extracts the thumbnail for the other albums.
        """
        path = settings.Paths.get_sm_thumb_path()

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
        processed = set(a.artisthash for a in SimilarArtistTable.get_all())

        # filter out artists that already have similar artists
        artists = filter(
            lambda a: a.artisthash not in processed, ArtistStore.get_flat_list()
        )
        artists = list(artists)

        with ProcessPoolExecutor(max_workers=max(1, os.cpu_count() // 2)) as executor:
            try:
                print("Processing similar artists")
                results = list(
                    tqdm(
                        executor.map(save_similar_artists, artists),
                        total=len(artists),
                        desc="Fetching similar artists",
                    )
                )

                list(results)
            # any exception that can be raised by the pool
            except Exception as e:
                log.warn(e)
                return
