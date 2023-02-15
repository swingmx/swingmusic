"""
This library contains the classes and functions related to the watchdog file watcher.
"""
import os
import sqlite3
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


from app.logger import log
from app.db.store import Store
from app.lib.taglib import get_tags
from app.models import Artist, Track
from app import settings

from app.db.sqlite.tracks import SQLiteManager
from app.db.sqlite.tracks import SQLiteTrackMethods as db
from app.db.sqlite.settings import SettingsSQLMethods as sdb


class Watcher:
    """
    Contains the methods for initializing and starting watchdog.
    """

    observers: list[Observer] = []

    def __init__(self):
        self.observer = Observer()

    def run(self):
        """
        Starts watchers for each dir in root_dirs
        """

        trials = 0

        while trials < 10:
            try:
                dirs = sdb.get_root_dirs()
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
            dirs = [settings.USER_HOME_DIR]

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


def add_track(filepath: str) -> None:
    """
    Processes the audio tags for a given file ands add them to the database and store.

    Then creates the folder, album and artist objects for the added track and adds them to the store.
    """
    tags = get_tags(filepath)

    if tags is None:
        return

    with SQLiteManager() as cur:
        db.remove_track_by_filepath(tags["filepath"])
        db.insert_one_track(tags, cur)

    track = Track(**tags)
    Store().add_track(track)

    Store.add_folder(track.folder)

    if not Store.album_exists(track.albumhash):
        album = Store.create_album(track)
        Store.add_album(album)

    artists: list[Artist] = track.artist + track.albumartist  # type: ignore

    for artist in artists:
        if not Store.artist_exists(artist.artisthash):
            Store.add_artist(Artist(artist.name))


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """
    try:
        track = Store.get_tracks_by_filepaths([filepath])[0]
    except IndexError:
        return

    db.remove_track_by_filepath(filepath)
    Store.remove_track_by_filepath(filepath)

    empty_album = Store.count_tracks_by_hash(track.albumhash) > 0

    if empty_album:
        Store.remove_album_by_hash(track.albumhash)

    artists: list[Artist] = track.artist + track.albumartist  # type: ignore

    for artist in artists:
        empty_artist = not Store.artist_has_tracks(artist.artisthash)

        if empty_artist:
            Store.remove_artist_by_hash(artist.artisthash)

    empty_folder = Store.is_empty_folder(track.folder)

    if empty_folder:
        Store.remove_folder(track.folder)


class Handler(PatternMatchingEventHandler):
    files_to_process = []
    files_to_process_windows = []

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
            case_sensitive=False,
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
            self.files_to_process.remove(event.src_path)
            if os.path.getsize(event.src_path) > 0:
                path = self.get_abs_path(event.src_path)
                add_track(path)
        except ValueError:
            pass

    def on_modified(self, event):
        # this event handler is triggered twice on windows
        # for copy events. We need to test how this behaves in
        # Linux.

        if event.src_path not in self.files_to_process_windows:
            return

        file_size = -1

        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(0.1)

        try:
            os.rename(event.src_path, event.src_path)
            path = self.get_abs_path(event.src_path)
            remove_track(path)
            add_track(path)
            self.files_to_process_windows.remove(event.src_path)
        except OSError:
            # File is locked, skipping
            pass
