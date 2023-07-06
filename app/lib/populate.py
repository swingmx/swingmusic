import json
import os
from collections import deque
from typing import Generator

from requests import ConnectionError as RequestConnectionError
from requests import ReadTimeout
from tqdm import tqdm

from app import settings
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.lastfm.similar_artists import SQLiteLastFMSimilarArtists as lastfmdb
from app.db.sqlite.settings import SettingsSQLMethods as sdb
from app.db.sqlite.tracks import SQLiteTrackMethods
from app.lib.artistlib import CheckArtistImages
from app.lib.colorlib import ProcessAlbumColors, ProcessArtistColors
from app.lib.taglib import extract_thumb, get_tags
from app.lib.trackslib import validate_tracks
from app.logger import log
from app.models import Album, Artist, Track
from app.models.lastfm import SimilarArtist
from app.requests.artists import fetch_similar_artists
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.filesystem import run_fast_scandir
from app.utils.network import Ping

get_all_tracks = SQLiteTrackMethods.get_all_tracks
insert_many_tracks = SQLiteTrackMethods.insert_many_tracks
remove_tracks_by_filepaths = SQLiteTrackMethods.remove_tracks_by_filepaths

POPULATE_KEY = ""


class PopulateCancelledError(Exception):
    pass


class Populate:
    """
    Populates the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to extract it.
    """

    def __init__(self, key: str) -> None:
        global POPULATE_KEY
        POPULATE_KEY = key

        validate_tracks()
        tracks = get_all_tracks()

        dirs_to_scan = sdb.get_root_dirs()

        if len(dirs_to_scan) == 0:
            log.warning(
                (
                    "The root directory is not configured. "
                    + "Open the app in your webbrowser to configure."
                )
            )
            return

        try:
            if dirs_to_scan[0] == "$home":
                dirs_to_scan = [settings.Paths.USER_HOME_DIR]
        except IndexError:
            pass

        files = set()

        for _dir in dirs_to_scan:
            files = files.union(run_fast_scandir(_dir, full=True)[1])

        unmodified = self.remove_modified(tracks)
        untagged = files - unmodified

        if len(untagged) != 0:
            self.tag_untagged(untagged, key)

        ProcessTrackThumbnails()
        ProcessAlbumColors()
        ProcessArtistColors()

        tried_to_download_new_images = False

        if Ping()():
            tried_to_download_new_images = True
            try:
                CheckArtistImages()
            except (RequestConnectionError, ReadTimeout):
                log.error(
                    "Internet connection lost. Downloading artist images stopped."
                )
        else:
            log.warning(
                f"No internet connection. Downloading artist images halted for {settings.get_scan_sleep_time()} seconds."
            )

        # Re-process the new artist images.
        if tried_to_download_new_images:
            ProcessArtistColors()

        if Ping()():
            FetchSimilarArtistsLastFM()

    @staticmethod
    def remove_modified(tracks: Generator[Track, None, None]):
        """
        Removes tracks from the database that have been modified
        since they were added to the database.
        """

        unmodified = set()
        modified = set()

        for track in tracks:
            try:
                if track.last_mod == os.path.getmtime(track.filepath):
                    unmodified.add(track.filepath)
                    continue
            except FileNotFoundError:
                print(f"File not found: {track.filepath}")
                TrackStore.tracks.remove(track)
                remove_tracks_by_filepaths(track.filepath)

            modified.add(track.filepath)

        TrackStore.remove_tracks_by_filepaths(modified)
        remove_tracks_by_filepaths(modified)

        return unmodified

    @staticmethod
    def tag_untagged(untagged: set[str], key: str):
        log.info("Found %s new tracks", len(untagged))
        tagged_tracks: deque[dict] = deque()
        tagged_count = 0

        fav_tracks = favdb.get_fav_tracks()
        fav_tracks = "-".join([t[1] for t in fav_tracks])

        for file in tqdm(untagged, desc="Reading files"):
            if POPULATE_KEY != key:
                raise PopulateCancelledError("Populate key changed")

            tags = get_tags(file)

            if tags is not None:
                tagged_tracks.append(tags)
                track = Track(**tags)
                track.is_favorite = track.trackhash in fav_tracks

                TrackStore.add_track(track)

                if not AlbumStore.album_exists(track.albumhash):
                    AlbumStore.add_album(AlbumStore.create_album(track))

                for artist in track.artist:
                    if not ArtistStore.artist_exists(artist.artisthash):
                        ArtistStore.add_artist(Artist(artist.name))

                for artist in track.albumartist:
                    if not ArtistStore.artist_exists(artist.artisthash):
                        ArtistStore.add_artist(Artist(artist.name))

                tagged_count += 1
            else:
                log.warning("Could not read file: %s", file)

        if len(tagged_tracks) > 0:
            log.info("Adding %s tracks to database", len(tagged_tracks))
            insert_many_tracks(tagged_tracks)

        log.info("Added %s/%s tracks", tagged_count, len(untagged))


def get_image(album: Album):
    """
    The function retrieves an image from an album by iterating through its tracks and extracting the thumbnail from the first track that has one.

    :param album: An instance of the `Album` class representing the album to retrieve the image from.
    :type album: Album
    :return: None
    """

    matching_tracks = filter(
        lambda t: t.albumhash == album.albumhash, TrackStore.tracks
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


from multiprocessing import Pool, cpu_count


class ProcessTrackThumbnails:
    """
    Extracts the album art from all albums in album store.
    """

    def __init__(self) -> None:
        with Pool(processes=cpu_count()) as pool:
            results = list(
                tqdm(
                    pool.imap_unordered(get_image, AlbumStore.albums),
                    total=len(AlbumStore.albums),
                    desc="Extracting track images",
                )
            )

            list(results)


def save_similar_artists(artist: Artist):
    """
    Downloads and saves similar artists to the database.
    """

    if lastfmdb.exists(artist.artisthash):
        return

    artist_hashes = fetch_similar_artists(artist.name)
    artist_ = SimilarArtist(artist.artisthash, "~".join(artist_hashes))

    if len(artist_.similar_artist_hashes) == 0:
        return

    lastfmdb.insert_one(artist_)


class FetchSimilarArtistsLastFM:
    """
    Fetches similar artists from LastFM using a process pool.
    """

    def __init__(self) -> None:
        artists = ArtistStore.artists

        with Pool(processes=cpu_count()) as pool:
            results = list(
                tqdm(
                    pool.imap_unordered(save_similar_artists, artists),
                    total=len(artists),
                    desc="Downloading similar artists",
                )
            )

            list(results)
