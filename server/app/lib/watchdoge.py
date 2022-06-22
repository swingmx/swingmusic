"""
This library contains the classes and functions related to the watchdog file watcher.
"""
import os
import time

from app.logger import logg
from app import instances
from app import models
from app.helpers import Get, create_album_hash
from app.lib.albumslib import create_album
from app.lib.taglib import get_tags
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class OnMyWatch:
    """
    Contains the methods for initializing and starting watchdog.
    """

    directory = os.path.expanduser("~")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive=True)

        try:
            self.observer.start()
        except OSError:
            logg.error("Could not start watchdog.")
            return

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


def add_track(filepath: str) -> None:
    """
    Processes the audio tags for a given file ands add them to the music dict.

    Then creates a folder object for the added track and adds it to api.FOLDERS
    """
    tags = get_tags(filepath)

    if tags is not None:
        hash = create_album_hash(tags["album"], tags["albumartist"])
        tags["albumhash"] = hash

        album = instances.album_instance.find_album_by_hash(hash)
        all_tracks = Get.get_all_tracks()
        all_tracks.append(models.Track(tags))

        if album is None:
            album_data = create_album(tags, all_tracks)
            album = models.Album(album_data)

            instances.album_instance.insert_album(album)

        tags["image"] = album.image
        instances.tracks_instance.insert_song(tags)


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """

    filepath = filepath + "k"

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
        print("🔵 created +++")
        self.files_to_process.append(event.src_path)

    def on_deleted(self, event):
        """
        Fired when a delete event occurs on a supported file.
        """
        print("🔴 deleted ---")
        remove_track(event.src_path)

    def on_moved(self, event):
        """
        Fired when a move event occurs on a supported file.
        """
        print("🔘 moved -->")
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
        print("⚫ closed ~~~")
        try:
            self.files_to_process.remove(event.src_path)
            add_track(event.src_path)
        except ValueError:
            """
            The file was already removed from the list, or it was not in the list to begin with.
            """
            pass


watch = OnMyWatch()

# TODO
# When removing a track, check if there are other tracks in the same album,
# if it was the last one, remove the album.
