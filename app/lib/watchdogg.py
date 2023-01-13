"""
This library contains the classes and functions related to the watchdog file watcher.
"""
import os
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from app.db.sqlite.tracks import SQLiteManager
from app.db.sqlite.tracks import SQLiteTrackMethods as db
from app.db.store import Store
from app.lib.taglib import get_tags
from app.logger import log
from app.models import Artist
from app.models import Track


class Watcher:
    """
    Contains the methods for initializing and starting watchdog.
    """

    home_dir = os.path.expanduser("~")
    dirs = [home_dir]
    observers: list[Observer] = []

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()

        for dir_ in self.dirs:
            self.observer.schedule(
                event_handler, os.path.realpath(dir_), recursive=True
            )
            self.observers.append(self.observer)

        try:
            self.observer.start()
        except OSError:
            log.error("Could not start watchdog.")
            return

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for obsv in self.observers:
                obsv.unschedule_all()
                obsv.stop()

        for obsv in self.observers:
            obsv.join()


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

    def __init__(self):
        log.info("✅ started watchdog")
        PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.flac", "*.mp3"],
            ignore_directories=True,
            case_sensitive=False,
        )

    def on_created(self, event):
        """
        Fired when a supported file is created.
        """
        self.files_to_process.append(event.src_path)

    def on_deleted(self, event):
        """
        Fired when a delete event occurs on a supported file.
        """

        remove_track(event.src_path)

    def on_moved(self, event):
        """
        Fired when a move event occurs on a supported file.
        """
        trash = "share/Trash"

        if trash in event.dest_path:
            remove_track(event.src_path)

        elif trash in event.src_path:
            add_track(event.dest_path)

        elif trash not in event.dest_path and trash not in event.src_path:
            add_track(event.dest_path)
            remove_track(event.src_path)

    def on_closed(self, event):
        """
        Fired when a created file is closed.
        """
        try:
            self.files_to_process.remove(event.src_path)
            if os.path.getsize(event.src_path) > 0:
                add_track(event.src_path)
        except ValueError:
            pass


# watcher = Watcher()
