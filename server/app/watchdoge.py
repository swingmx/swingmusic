import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class OnMyWatch:
    watchDirectory = "/home/cwilvx/Music"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


def create_thumb_dir(filepath):
    f_name = filepath.split('/')[-1]
    parent_dir = filepath.replace(f_name, '')

    thumb_dir = parent_dir + ".thumbnails"

    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)


class Handler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(
            self, patterns=['*.flac', '*.mp3'], ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        print(event.src_path)
        create_thumb_dir(event.src_path)

    def on_deleted(self, event):
        print(event.src_path)

    def on_moved(self, event):
        print(event.src_path)
        print(event.dest_path)


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
