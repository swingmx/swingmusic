from dataclasses import asdict
from os import path

from app import api
from app import settings
from app.helpers import run_fast_scandir
from app.instances import album_instance
from app.instances import tracks_instance
from app.lib import folderslib
from app.lib.albumslib import create_album
from app.lib.albumslib import find_album
from app.lib.taglib import get_tags
from app.logger import Log
from app.models import Track
from progress.bar import Bar


class Populate:
    """
    Populate the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to
    extract it.
    """

    def __init__(self) -> None:
        self.files = []
        self.db_tracks = []
        self.tagged_tracks = []
        self.folders = set()
        self.pre_albums = []
        self.albums = []

        self.files = run_fast_scandir(settings.HOME_DIR, [".flac", ".mp3"])[1]
        self.db_tracks = tracks_instance.get_all_tracks()

    def run(self):
        self.check_untagged()

        if len(self.files) == 0:
            return

        self.tag_files()
        self.create_pre_albums()
        self.create_albums()
        self.create_tracks()
        self.create_folders()

    def check_untagged(self):
        """
        Loops through all the tracks in db tracks removing each
        from the list of tagged tracks if it exists.
        We will now only have untagged tracks left in `files`.
        """
        bar = Bar("Checking untagged", max=len(self.db_tracks))
        for track in self.db_tracks:
            if track["filepath"] in self.files:
                self.files.remove(track["filepath"])
            bar.next()

        bar.finish()
        Log(f"Found {len(self.files)} untagged tracks")

    def tag_files(self):
        """
        Loops through all the untagged files and tags them.
        """
        bar = Bar("Tagging files", max=len(self.files))
        for file in self.files:
            tags = get_tags(file)
            folder = path.dirname(file)
            self.folders.add(folder)

            if tags is not None:
                self.tagged_tracks.append(tags)
                api.DB_TRACKS.append(tags)

            bar.next()
        bar.finish()
        Log(f"Tagged {len(self.tagged_tracks)} files")

    def create_pre_albums(self):
        """
        Creates pre-albums for the all tagged tracks.
        """
        bar = Bar("Creating pre-albums", max=len(self.tagged_tracks))
        for track in self.tagged_tracks:
            album = {"title": track["album"], "artist": track["albumartist"]}

            if album not in self.pre_albums:
                self.pre_albums.append(album)
            bar.next()

        bar.finish()
        Log(f"Created {len(self.pre_albums)} pre-albums")

    def create_albums(self):
        """
        Uses the pre-albums to create new albums and add them to the database.
        """
        exist_count = 0

        bar = Bar("Creating albums", max=len(self.pre_albums))
        for album in self.pre_albums:
            index = find_album(album["title"], album["artist"])

            if index is None:
                try:
                    track = [
                        track for track in self.tagged_tracks
                        if track["album"] == album["title"]
                        and track["albumartist"] == album["artist"]
                    ][0]

                    album = create_album(track)
                    api.ALBUMS.append(album)
                    self.albums.append(album)

                    album_instance.insert_album(asdict(album))

                except IndexError:
                    print("😠\n")
                    print(album)

            else:
                exist_count += 1

            bar.next()
        bar.finish()
        Log(f"{exist_count} of {len(self.pre_albums)} albums were already in the database"
            )

    def create_tracks(self):
        """
        Loops through all the tagged tracks creating complete track objects using the `models.Track` model.
        """
        bar = Bar("Creating tracks", max=len(self.tagged_tracks))
        failed_count = 0
        for track in self.tagged_tracks:
            try:
                album_index = find_album(track["album"], track["albumartist"])
                album = api.ALBUMS[album_index]
                track["image"] = album.image
                upsert_id = tracks_instance.insert_song(track)
                track["_id"] = {"$oid": str(upsert_id)}
                api.TRACKS.append(Track(track))
            except:
                # Bug: some albums are not found although they exist in `api.ALBUMS`. It has something to do with the bisection method used or sorting. Not sure yet.
                failed_count += 1
            bar.next()
        bar.finish()

        Log(f"Added {len(self.tagged_tracks) - failed_count} of {len(self.tagged_tracks)} new tracks and {len(self.albums)} new albums"
            )

    def create_folders(self):
        """
        Creates the folder objects for all the tracks.
        """
        bar = Bar("Creating folders", max=len(self.folders))
        old_f_count = len(api.FOLDERS)
        for folder in self.folders:
            api.VALID_FOLDERS.add(folder)
            fff = folderslib.create_folder(folder)
            api.FOLDERS.append(fff)
            bar.next()

        bar.finish()

        Log(f"Created {len(self.folders)} new folders")
