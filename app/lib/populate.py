from dataclasses import asdict
import os
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Generator

from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout

from app import settings
from app.db.libdata import ArtistTable
from app.db.libdata import AlbumTable, TrackTable
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb

# from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as lastfmdb
from app.db.sqlite.tracks import SQLiteTrackMethods
from app.lib.artistlib import CheckArtistImages
from app.lib.colorlib import ProcessArtistColors
from app.lib.errors import PopulateCancelledError
from app.lib.taglib import extract_thumb
from app.logger import log
from app.models import Album, Artist, Track
from app.models.lastfm import SimilarArtist
from app.requests.artists import fetch_similar_artists
from app.utils.filesystem import run_fast_scandir
from app.utils.network import has_connection
from app.utils.progressbar import tqdm

from app.db.userdata import SimilarArtistTable

get_all_tracks = SQLiteTrackMethods.get_all_tracks
insert_many_tracks = SQLiteTrackMethods.insert_many_tracks
remove_tracks_by_filepaths = SQLiteTrackMethods.remove_tracks_by_filepaths

POPULATE_KEY = ""


class Populate:
    """
    Populates the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to extract it.
    """

    # def __init__(self, instance_key: str) -> None:
    # return

    # if len(dirs_to_scan) == 0:
    #     log.warning(
    #         (
    #             "The root directory is not configured. "
    #             + "Open the app in your webbrowser to configure."
    #         )
    #     )
    #     return

    # try:
    #     if dirs_to_scan[0] == "$home":
    #         dirs_to_scan = [settings.Paths.USER_HOME_DIR]
    # except IndexError:
    #     pass

    # files = set()

    # for _dir in dirs_to_scan:
    #     files = files.union(run_fast_scandir(_dir, full=True)[1])

    # unmodified, modified_tracks = self.remove_modified(tracks)
    # untagged = files - unmodified

    # if len(untagged) != 0:
    #     self.tag_untagged(untagged, instance_key)

    # self.extract_thumb_with_overwrite(modified_tracks)


class CordinateMedia:
    """
    Cordinates the extracting of thumbnails
    """

    def __init__(self, instance_key: str):
        global POPULATE_KEY
        POPULATE_KEY = instance_key

        try:
            ProcessTrackThumbnails(instance_key)
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

    # @staticmethod
    # def remove_modified(tracks: Generator[TrackTable, None, None]):
    #     """
    #     Removes tracks from the database that have been modified
    #     since they were added to the database.
    #     """

    #     unmodified_paths = set()
    #     modified_tracks: list[TrackTable] = []
    #     modified_paths = set()

    #     for track in tracks:
    #         try:
    #             if track.last_mod == round(os.path.getmtime(track.filepath)):
    #                 unmodified_paths.add(track.filepath)
    #                 continue
    #         except (FileNotFoundError, OSError) as e:
    #             log.warning(e)  # REVIEW More informations = good
    #             TrackStore.remove_track_obj(track)
    #             remove_tracks_by_filepaths(track.filepath)

    #         modified_paths.add(track.filepath)
    #         modified_tracks.append(track)

    #     TrackStore.remove_tracks_by_filepaths(modified_paths)
    #     remove_tracks_by_filepaths(modified_paths)

    #     return unmodified_paths, modified_tracks

    # @staticmethod
    # def tag_untagged(untagged: set[str], key: str):
    #     pass
    # for file in tqdm(untagged, desc="Reading files"):
    #     if POPULATE_KEY != key:
    #         log.warning("'Populate.tag_untagged': Populate key changed")
    #         return

    #     tags = get_tags(file)

    #     if tags is not None:
    #         TrackTable.insert_one(tags)

    # =============================================

    # log.info("Found %s new tracks", len(untagged))
    # # tagged_tracks: deque[dict] = deque()
    # # tagged_count = 0

    # favs = favdb.get_fav_tracks()
    # records = dict()

    # for fav in favs:
    #     r = records.setdefault(fav[1], set())
    #     r.add(fav[4])

    #     tagged_tracks.append(tags)
    #     track = Track(**tags)

    #     track.fav_userids = list(records.get(track.trackhash, set()))

    #     TrackStore.add_track(track)

    #     if not AlbumStore.album_exists(track.albumhash):
    #         AlbumStore.add_album(AlbumStore.create_album(track))

    #     for artist in track.artists:
    #         if not ArtistStore.artist_exists(artist.artisthash):
    #             ArtistStore.add_artist(Artist(artist.name))

    #     for artist in track.albumartists:
    #         if not ArtistStore.artist_exists(artist.artisthash):
    #             ArtistStore.add_artist(Artist(artist.name))

    #     tagged_count += 1
    # else:
    #     log.warning("Could not read file: %s", file)

    # if len(tagged_tracks) > 0:
    #     log.info("Adding %s tracks to database", len(tagged_tracks))
    #     insert_many_tracks(tagged_tracks)

    # log.info("Added %s/%s tracks", tagged_count, len(untagged))

    # @staticmethod
    # def extract_thumb_with_overwrite(tracks: list[TrackTable]):
    #     """
    #     Extracts the thumbnail from a list of filepaths,
    #     overwriting the existing thumbnail if it exists,
    #     for modified files.
    #     """
    #     for track in tracks:
    #         try:
    #             extract_thumb(track.filepath, track.image, overwrite=True)
    #         except FileNotFoundError:
    #             continue


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

    matching_tracks = filter(
        lambda t: t.albumhash == album.albumhash,
        TrackTable.get_tracks_by_albumhash(album.albumhash),
    )

    try:
        track = next(matching_tracks)
        extracted = extract_thumb(track.filepath, track.image)

        while not extracted:
            try:
                track = next(matching_tracks)
                extracted = extract_thumb(track.filepath, track.image)
            except StopIteration:
                break

        return
    except StopIteration:
        pass


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
            lambda album: album.albumhash not in processed, AlbumTable.get_all()
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
        artists = filter(lambda a: a.artisthash not in processed, ArtistTable.get_all())
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
