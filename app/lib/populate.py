from dataclasses import asdict
import os
from concurrent.futures import ThreadPoolExecutor

from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from app import settings
from app.lib.artistlib import CheckArtistImages
from app.lib.colorlib import ProcessAlbumColors, ProcessArtistColors
from app.lib.errors import PopulateCancelledError
from app.lib.taglib import extract_thumb
from app.logger import log
from app.models import Album, Artist
from app.models.lastfm import SimilarArtist
from app.requests.artists import fetch_similar_artists
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.utils.network import has_connection
from app.utils.progressbar import tqdm

from app.db.userdata import SimilarArtistTable


POPULATE_KEY = ""


class CordinateMedia:
    """
    Cordinates the extracting of thumbnails
    """

    def __init__(self, instance_key: str):
        global POPULATE_KEY
        POPULATE_KEY = instance_key

        try:
            ProcessTrackThumbnails(instance_key)
            ProcessAlbumColors(instance_key)
            ProcessArtistColors(instance_key)
        except PopulateCancelledError as e:
            log.warn(e)
            return

        tried_to_download_new_images = False

        if has_connection():
            tried_to_download_new_images = True
            try:
                CheckArtistImages(instance_key)
            except (RequestConnectionError, ReadTimeout) as e:
                log.error(
                    "Internet connection lost. Downloading artist images suspended."
                )
                log.error(e)  # REVIEW More informations = good
        else:
            log.warning(f"No internet connection. Downloading artist images suspended!")

        # Re-process the new artist images.
        if tried_to_download_new_images:
            ProcessArtistColors(instance_key=instance_key)

        if has_connection():
            try:
                print("Attempting to download similar artists...")
                FetchSimilarArtistsLastFM(instance_key)
            except PopulateCancelledError as e:
                log.warn(e)
                return


def get_image(_map: tuple[str, Album]):
    """
    The function retrieves an image from an album by iterating through its tracks and extracting the thumbnail from the first track that has one.

    :param album: An instance of the `Album` class representing the album to retrieve the image from.
    :type album: Album
    :return: None
    """

    instance_key, album = _map

    if POPULATE_KEY != instance_key:
        raise PopulateCancelledError("'ProcessTrackThumbnails': Populate key changed")

    matching_tracks = AlbumStore.get_album_tracks(album.albumhash)

    for track in matching_tracks:
        if extract_thumb(track.filepath, track.image):
            break


def get_cpu_count():
    """
    Returns the number of CPUs on the machine.
    """
    cpu_count = os.cpu_count() or 0
    return cpu_count // 2 if cpu_count > 2 else cpu_count


class ProcessTrackThumbnails:
    """
    Extracts the album art from all albums in album store.
    """

    def __init__(self, instance_key: str) -> None:
        """
        Filters out albums that already have thumbnails and
        extracts the thumbnail for the other albums.
        """
        path = settings.Paths.get_sm_thumb_path()

        # read all the files in the thumbnail directory
        processed = "".join(os.listdir(path)).replace("webp", "")

        # filter out albums that already have thumbnails
        albums = filter(
            lambda album: album.albumhash not in processed, AlbumStore.get_flat_list()
        )
        albums = list(albums)

        # process the rest
        key_album_map = ((instance_key, album) for album in albums)

        with ThreadPoolExecutor(max_workers=get_cpu_count()) as executor:
            results = list(
                tqdm(
                    executor.map(get_image, key_album_map),
                    total=len(albums),
                    desc="Extracting track images",
                )
            )

            list(results)


def save_similar_artists(_map: tuple[str, Artist]):
    """
    Downloads and saves similar artists to the database.
    """

    instance_key, artist = _map

    if POPULATE_KEY != instance_key:
        print("Warning: Populate key changed")
        raise PopulateCancelledError(
            "'FetchSimilarArtistsLastFM': Populate key changed"
        )

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

    def __init__(self, instance_key: str) -> None:
        # read all artists from db
        processed = SimilarArtistTable.get_all()
        processed = ".".join(a.artisthash for a in processed)

        # filter out artists that already have similar artists
        artists = filter(
            lambda a: a.artisthash not in processed, ArtistStore.get_flat_list()
        )
        artists = list(artists)

        # process the rest
        key_artist_map = ((instance_key, artist) for artist in artists)

        with ThreadPoolExecutor(max_workers=get_cpu_count()) as executor:
            try:
                print("Processing similar artists")
                results = list(
                    tqdm(
                        executor.map(save_similar_artists, key_artist_map),
                        total=len(artists),
                        desc="Fetching similar artists",
                    )
                )

                list(results)

            except PopulateCancelledError as e:
                raise e

            # any exception that can be raised by the pool
            except Exception as e:
                log.warn(e)
                return
