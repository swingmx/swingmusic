"""
This library contains the classes and functions related to the watchdog file watcher.
"""

import json
import os
import sqlite3
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.api import BaseObserverSubclassCallable
from watchdog.observers import Observer

from swingmusic import settings
from swingmusic.config import UserConfig
from swingmusic.db.libdata import TrackTable
from swingmusic.db.userdata import LibDataTable
from swingmusic.lib.colorlib import process_color
from swingmusic.lib.tagger import create_albums, create_artists
from swingmusic.lib.taglib import extract_thumb, get_tags
from swingmusic.logger import log
from swingmusic.models import Artist, Track
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistMapEntry, ArtistStore
from swingmusic.store.tracks import TrackStore


class Watcher:
    """
    Contains the methods for initializing and starting watchdog.
    """

    observers: list[BaseObserverSubclassCallable] = []

    def __init__(self):
        self.observer = Observer()

    def run(self):
        """
        Starts watchers for each dir in root_dirs
        """

        trials = 0

        while trials < 10:
            try:
                # dirs = sdb.get_root_dirs()
                dirs = UserConfig().rootDirs
                dirs = [rf"{d}" for d in dirs]

                dir_map = [
                    {"original": d, "realpath": os.path.realpath(d)} for d in dirs
                ]
                break
            except sqlite3.OperationalError:
                trials += 1
                time.sleep(1)
        else:
            log.error(
                "WatchDogError: Failed to start Watchdog. Waiting for database timed out!"
            )
            return

        if len(dirs) == 0:
            log.warning(
                "WatchDogInfo: No root directories configured. Watchdog not started."
            )
            return

        dir_map = [d for d in dir_map if d["realpath"] != d["original"]]

        # if len(dirs) > 0 and dirs[0] == "$home":
        #     dirs = [settings.USER_HOME_DIR]

        if any([d == "$home" for d in dirs]):
            dirs = [settings.Paths.USER_HOME_DIR]

        event_handler = Handler(root_dirs=dirs, dir_map=dir_map)

        for _dir in dirs:
            exists = os.path.exists(_dir)

            if not exists:
                log.error("WatchdogError: Directory not found: %s", _dir)

        for _dir in dirs:
            self.observer.schedule(
                event_handler, os.path.realpath(_dir), recursive=True
            )
            self.observers.append(self.observer)

        try:
            self.observer.start()
            log.info("Started watchdog")
        except (FileNotFoundError, PermissionError):
            log.error(
                "WatchdogError: Failed to start watchdog,  root directories could not be resolved."
            )
            return
        except OSError as e:
            log.error("Failed to start watchdog. %s", e)
            return

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_all()

        for obsv in self.observers:
            obsv.join()

    def stop_all(self):
        """
        Unschedules and stops all existing watchers.
        """
        log.info("Stopping all watchdog observers")
        for obsv in self.observers:
            obsv.unschedule_all()
            obsv.stop()

    def restart(self):
        """
        Stops all existing watchers, refetches root_dirs from the db
        and restarts the watchers.
        """
        log.info("🔃 Restarting watchdog")
        self.stop_all()
        self.run()


def handle_color(albumhash: str):
    entry = LibDataTable.find_one(albumhash, "album")

    if entry and entry.color:
        return

    colors = process_color(albumhash, is_album=True)

    if colors is None:
        return

    if entry is None:
        LibDataTable.insert_one(
            {"itemhash": albumhash, "color": colors[0], "itemtype": "album"}
        )
    else:
        LibDataTable.update_one(albumhash, {"color": colors[0]})

    return colors


def add_track(filepath: str) -> None:
    """
    Processes the audio tags for a given file ands add them to the database and store.

    Then creates the folder, album and artist objects for the added track and adds them to the store.
    """

    TrackStore.remove_track_by_filepath(filepath)

    config = UserConfig()
    tags = get_tags(filepath, config)

    # if the track is somehow invalid, return
    if tags is None or tags["bitrate"] == 0 or tags["duration"] == 0:
        return

    TrackTable.insert_one(tags)
    extract_thumb(filepath, tags["albumhash"] + ".webp", overwrite=True)

    colors = handle_color(tags["albumhash"])
    track = Track(**tags)
    TrackStore.add_track(track)

    # SECTION: Index album
    albumentry = AlbumStore.albummap.get(track.albumhash)

    if albumentry is None:
        album, trackhashes = create_albums([track.trackhash])[0]
        AlbumStore.index_new_album(album, trackhashes)
    else:
        trackhash_exists = track.trackhash in albumentry.trackhashes

        if not trackhash_exists:
            albumentry.trackhashes.add(track.trackhash)
            albumentry.album.trackcount += 1
            albumentry.set_color(colors[0]) if colors else None

    # SECTION: Index artist
    artists = create_artists(track.artisthashes)

    for artist in artists:
        ArtistStore.artistmap[artist[0].artisthash] = ArtistMapEntry(
            artist=artist[0],
            albumhashes=artist[1],
            trackhashes=artist[2],
        )


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """
    try:
        track = TrackStore.get_tracks_by_filepaths([filepath])[0]
    except IndexError:
        return

    db.remove_tracks_by_filepaths(filepath)
    TrackStore.remove_track_by_filepath(filepath)

    empty_album = TrackStore.count_tracks_by_trackhash(track.albumhash) > 0

    if empty_album:
        AlbumStore.remove_album_by_hash(track.albumhash)

    artists: list[Artist] = track.artists + track.albumartists  # type: ignore

    for artist in artists:
        empty_artist = not ArtistStore.artist_has_tracks(artist.artisthash)

        if empty_artist:
            ArtistStore.remove_artist_by_hash(artist.artisthash)


class Handler(PatternMatchingEventHandler):
    files_to_process = []
    files_to_process_windows = []
    file_sizes = {}

    root_dirs = []
    dir_map = []

    def __init__(self, root_dirs: list[str], dir_map: dict[str:str]):
        self.root_dirs = root_dirs
        self.dir_map = dir_map
        patterns = [f"*{f}" for f in settings.SUPPORTED_FILES]

        PatternMatchingEventHandler.__init__(
            self,
            patterns=patterns,
            ignore_directories=True,
        )

    def get_abs_path(self, path: str):
        """
        Convert a realpath to a path relative to the matching root directory.
        """
        for d in self.dir_map:
            if d["realpath"] in path:
                return path.replace(d["realpath"], d["original"])

        return path

    def on_created(self, event):
        """
        Fired when a supported file is created.
        """
        try:
            self.file_sizes[event.src_path] = os.path.getsize(event.src_path)
        except FileNotFoundError:
            return

        self.files_to_process.append(event.src_path)
        self.files_to_process_windows.append(event.src_path)

    def on_deleted(self, event):
        """
        Fired when a delete event occurs on a supported file.
        """
        path = self.get_abs_path(event.src_path)
        remove_track(path)

    def on_moved(self, event):
        """
        Fired when a move event occurs on a supported file.
        """
        trash = "share/Trash"

        if trash in event.dest_path:
            path = self.get_abs_path(event.src_path)
            remove_track(path)

        elif trash in event.src_path:
            path = self.get_abs_path(event.dest_path)
            add_track(path)

        elif trash not in event.dest_path and trash not in event.src_path:
            dest_path = self.get_abs_path(event.dest_path)
            src_path = self.get_abs_path(event.src_path)

            add_track(dest_path)
            remove_track(src_path)

    def on_closed(self, event):
        """
        Fired when a created file is closed.
        NOT FIRED IN WINDOWS
        """
        try:
            # Get initial file size
            initial_size = os.path.getsize(event.src_path)

            # Wait for 10 seconds
            time.sleep(10)

            # Check if file size has changed
            current_size = os.path.getsize(event.src_path)

            if current_size > 0 and current_size == initial_size:
                path = self.get_abs_path(event.src_path)
                add_track(path)
                # Remove from processing list only after successful processing
                self.files_to_process.remove(event.src_path)
            else:
                # File is still being modified or has been deleted
                log.info(
                    f"File {event.src_path} is still being modified. Skipping processing for now."
                )
        except FileNotFoundError:
            # file was closed and deleted.
            log.info(f"File {event.src_path} was closed and deleted before processing.")
        except ValueError:
            # file was already removed from the list by another event handler.
            log.info(
                f"File {event.src_path} was already removed from the processing list."
            )

    def on_modified(self, event):
        # this event handler is triggered twice on windows
        # for copy events. We need to test how this behaves in
        # Linux.

        if event.src_path not in self.files_to_process_windows:
            return

        # Check if file write operation is complete
        try:
            current_size = os.path.getsize(event.src_path)
        except FileNotFoundError:
            # File was deleted or moved
            return

        previous_size = self.file_sizes.get(event.src_path, -1)

        if current_size == previous_size:
            # Wait for a short duration to ensure the file write operation is complete
            time.sleep(10)

            # Check the file size again
            try:
                current_size = os.path.getsize(event.src_path)
            except FileNotFoundError:
                # File was deleted or moved
                return

            if current_size == previous_size:
                try:
                    os.rename(event.src_path, event.src_path)
                    path = self.get_abs_path(event.src_path)
                    remove_track(path)
                    add_track(path)
                    self.files_to_process_windows.remove(event.src_path)
                    del self.file_sizes[event.src_path]
                except OSError:
                    # File is locked
                    pass
                return

        # Update the file size for the next iteration
        self.file_sizes[event.src_path] = current_size
