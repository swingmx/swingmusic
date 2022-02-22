from pprint import pprint
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from app import instances, functions
from app import api


class OnMyWatch:
    directory = os.path.expanduser("~")

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory, recursive=True)
        self.observer.start()

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
    """
    tags = functions.get_tags(filepath)
    print(tags)

    if tags is not None:
        instances.songs_instance.insert_song(tags)
        track = instances.songs_instance.get_song_by_path(tags["filepath"])

        track_obj = functions.create_track_class(track)
        api.all_the_f_music.append(track_obj)


def remove_track(filepath: str) -> None:
    """
    Removes a track from the music dict.
    """
    trackid = instances.songs_instance.get_song_by_path(filepath)["_id"]["$oid"]
    instances.songs_instance.remove_song_by_id(trackid)

    for track in api.all_the_f_music:
        if track.trackid == trackid:
            api.all_the_f_music.remove(track)


class Handler(PatternMatchingEventHandler):
    files_to_process = []

    def __init__(self):
        print("💠 started watchdog")
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
        self.files_to_process.remove(event.src_path)
        add_track(event.src_path)


watch = OnMyWatch()
