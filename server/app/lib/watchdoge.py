"""
This library contains the classes and functions related to the watchdog file watcher.
"""
import os
import time
from typing import List

from app import instances
from app.helpers import create_hash
from app.lib.taglib import get_tags
from app.logger import get_logger
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

log = get_logger()


class OnMyWatch:
    """
    Contains the methods for initializing and starting watchdog.
    """

    home_dir = os.path.expanduser("~")
    dirs = [home_dir]
    observers: List[Observer] = []

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()

        for dir in self.dirs:
            print("something")
            self.observer.schedule(event_handler, os.path.realpath(dir), recursive=True)
            self.observers.append(self.observer)

        try:
            self.observer.start()
            print("something something")
        except OSError:
            log.error("Could not start watchdog.")
            return

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for o in self.observers:
                o.unschedule_all()
                o.stop()
            print("Observer Stopped")

        for o in self.observers:
            o.join()


def add_track(filepath: str) -> None:
    """
    Processes the audio tags for a given file ands add them to the music dict.

    Then creates a folder object for the added track and adds it to api.FOLDERS
    """
    tags = get_tags(filepath)

    if tags is not None:
        hash = create_hash(tags["album"], tags["albumartist"])
        tags["albumhash"] = hash
        instances.tracks_instance.insert_song(tags)


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """

    instances.tracks_instance.remove_song_by_filepath(filepath)


class Handler(PatternMatchingEventHandler):
    files_to_process = []

    def __init__(self):
        print("💠 started watchdog 💠")
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
        print("💠 created file 💠")
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
        tr = "share/Trash"

        if tr in event.dest_path:
            print("trash ++")
            remove_track(event.src_path)

        elif tr in event.src_path:
            add_track(event.dest_path)

        elif tr not in event.dest_path and tr not in event.src_path:
            add_track(event.dest_path)
            remove_track(event.src_path)

    def on_closed(self, event):
        """
        Fired when a created file is closed.
        """
        try:
            self.files_to_process.remove(event.src_path)
            add_track(event.src_path)
        except ValueError:
            """
            The file was already removed from the list, or it was not in the list to begin with.
            """
            pass


watch = OnMyWatch()
