import os
import time
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from multiprocessing import Pool
from os import path
from typing import List

from app import api
from app import settings
from app.helpers import create_album_hash
from app.helpers import run_fast_scandir
from app.instances import album_instance
from app.instances import tracks_instance
from app.lib import folderslib
from app.lib.albumslib import create_album
from app.lib.albumslib import find_album
from app.lib.taglib import get_tags
from app.lib.trackslib import find_track
from app.logger import Log
from app.models import Album
from app.models import Track
from tqdm import tqdm


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
        self.albums: List[Album] = []

        self.files = run_fast_scandir(settings.HOME_DIR, full=True)[1]
        self.db_tracks = tracks_instance.get_all_tracks()
        self.tag_count = 0
        self.exist_count = 0

    def run(self):
        self.check_untagged()
        self.get_all_tags()

        if len(self.tagged_tracks) == 0:
            return

        self.tagged_tracks.sort(key=lambda x: x["albumhash"])
        self.tracks = deepcopy(self.tagged_tracks)

        self.create_pre_albums()
        self.create_albums()

        self.albums.sort(key=lambda x: x.hash)
        api.ALBUMS.sort(key=lambda x: x.hash)

        self.save_albums()
        self.create_tracks()
        self.create_folders()

    def check_untagged(self):
        """
        Loops through all the tracks in db tracks removing each
        from the list of tagged tracks if it exists.
        We will now only have untagged tracks left in `files`.
        """
        for track in tqdm(self.db_tracks, desc="Checking untagged"):
            if track["filepath"] in self.files:
                self.files.remove(track["filepath"])

        Log(f"Found {len(self.files)} untagged tracks")

    def process_tags(self, tags: dict):
        for t in tags:
            if t is None:
                continue

            t["albumhash"] = create_album_hash(t["album"], t["albumartist"])
            self.tagged_tracks.append(t)
            api.DB_TRACKS.append(t)

            self.folders.add(t["folder"])

    def get_tags(self, file: str):
        tags = get_tags(file)

        if tags is not None:
            folder = tags["folder"]
            self.folders.add(folder)

            tags["albumhash"] = create_album_hash(tags["album"], tags["albumartist"])
            self.tagged_tracks.append(tags)
            api.DB_TRACKS.append(tags)

    def get_all_tags(self):
        """
        Loops through all the untagged files and tags them.
        """

        s = time.time()
        print(f"Started tagging files")
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_tags, self.files)

        # with Pool(maxtasksperchild=10, processes=10) as p:
        #     tags = p.map(get_tags, tqdm(self.files))
        #     self.process_tags(tags)

        # for t in tqdm(self.files):
        #     self.get_tags(t)

        d = time.time() - s
        Log(f"Tagged {len(self.tagged_tracks)} files in {d} seconds")

    def create_pre_albums(self):
        """
        Creates pre-albums for the all tagged tracks.
        """
        for track in tqdm(self.tagged_tracks, desc="Creating pre-albums"):
            album = {"title": track["album"], "artist": track["albumartist"]}

            if album not in self.pre_albums:
                self.pre_albums.append(album)

        Log(f"Created {len(self.pre_albums)} pre-albums")

    def create_album(self, album: dict):
        albumhash = create_album_hash(album["title"], album["artist"])
        index = find_album(api.ALBUMS, albumhash)

        if index is not None:
            album = api.ALBUMS[index]
            self.albums.append(album)

            self.exist_count += 1
            return

        self.albums.sort(key=lambda x: x.hash)
        index = find_track(self.tagged_tracks, albumhash)

        if index is None:
            return

        track = self.tagged_tracks[index]

        album = create_album(track, self.tagged_tracks)

        if album is None:
            print("album is none")
            return

        album = Album(album)

        api.ALBUMS.append(album)
        self.albums.append(album)

    def create_albums(self):
        """
        Uses the pre-albums to create new albums and add them to the database.
        """
        for album in tqdm(self.pre_albums, desc="Building albums"):
            self.create_album(album)

        Log(
            f"{self.exist_count} of {len(self.pre_albums)} albums were already in the database"
        )

    def create_track(self, track: dict):
        """
        Creates a single track object.
        """

        albumhash = track["albumhash"]
        index = find_album(self.albums, albumhash)

        if index is None:
            return

        try:
            album: Album = self.albums[index]
        except (TypeError):
            """
            😭😭😭
            """
            pass

        track["image"] = album.image

        upsert_id = tracks_instance.insert_song(track)
        track["_id"] = {"$oid": str(upsert_id)}

        api.TRACKS.append(Track(track))

    def create_tracks(self):
        """
        Loops through all the tagged tracks creating complete track objects using the `models.Track` model.
        """
        with ThreadPoolExecutor() as executor:
            executor.map(self.create_track, self.tagged_tracks)

        Log(
            f"Added {len(self.tagged_tracks)} new tracks and {len(self.albums)} new albums"
        )

    def save_albums(self):
        """
        Saves the albums to the database.
        """

        with ThreadPoolExecutor() as executor:
            executor.map(album_instance.insert_album, self.albums)

    def create_folders(self):
        """
        Creates the folder objects for all the tracks.
        """
        for folder in tqdm(self.folders, desc="Creating folders"):
            api.VALID_FOLDERS.add(folder)

            fff = folderslib.create_folder(folder)
            api.FOLDERS.append(fff)

        Log(f"Created {len(self.folders)} new folders")
