import os, sys, logging, time

from io import BytesIO
from pathlib import Path

import PIL

from watchdog import observers

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

from mutagen.mp3 import MP3, MutagenError
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from PIL import Image

music_dir = "/home/cwilvx/Music/"
folders = os.listdir(music_dir)


def updateThumbnails():
    start_time = time.time()
    print("Updating thumbnails ...")

    for folder in folders:
        print(folder)
        try:
            dir = music_dir + folder
            thumbnail_folder = dir + "/"+ ".thumbnails"

            if not os.path.exists(thumbnail_folder):
                os.makedirs(thumbnail_folder)

            def thumbnail_extractor(type, song):
                if type == "mp3":
                    tags = ID3(song)
                    image_path = "{}/.thumbnails/{}".format(dir, song.name.replace(".mp3", ".jpg"))
                    album_art = tags.getall('APIC')[0].data
                elif type == "flac":
                    tags = FLAC(song)
                    image_path = "{}/.thumbnails/{}".format(dir, song.name.replace(".flac", ".jpg"))
                    album_art = tags.pictures[0].data
                else:
                    print("Unsupported file type")
                    return
                
                image = Image.open(BytesIO(album_art))

                if not os.path.exists(image_path):
                    try:
                        image.save(image_path, 'JPEG')
                    except OSError:
                        image.convert('RGB').save(image_path, 'JPEG')

            for song in Path(dir).rglob('*.mp3'):
                try:
                    thumbnail_extractor("mp3", song)
                except (MutagenError, IndexError):
                    pass
            for song in Path(dir).rglob('*.flac'):
                try:
                    thumbnail_extractor("flac", song)
                except (MutagenError, IndexError):
                    pass
        except NotADirectoryError:
            pass
            
        print("done")

    print("Done in: %s seconds" % round((time.time() - start_time), 1))


class watchMusicDirs(FileSystemEventHandler):
    def __init__(self, logger=None):
        super().__init__()

        self.logger = logger or logging.root

    # def on_moved(self, event):
    #     super().on_moved(event)

    #     what = 'directory' if event.is_directory else 'file'
    #     self.logger.info("Moved %s: from %s to %s", what, event.src_path,
    #                      event.dest_path)

    # def on_created(self, event):
    #     super().on_created(event)

    #     what = 'directory' if event.is_directory else 'file'
    #     self.logger.info("Created %s: %s", what, event.src_path)

    # def on_deleted(self, event):
    #     super().on_deleted(event)

    #     what = 'directory' if event.is_directory else 'file'
    #     self.logger.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        # self.logger.info("Modified %s: %s", what, event.src_path)
        print("Modified %s: %s" % (what, event.src_path))
        updateThumbnails()

paths = [music_dir, '/home/cwilvx/watched']

if __name__ == "__main__":
    observer = Observer()
    event_handler = watchMusicDirs()

    observers = []

    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
        observers.append(observer)

    observer.start()

    try:
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        for observer in observers:
            observer.unschedule_all()

            observer.stop()
    
    for observer in observers:
        observer.join()