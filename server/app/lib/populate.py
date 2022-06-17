import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from app import settings
from app.helpers import create_album_hash
from app.helpers import run_fast_scandir
from app.instances import album_instance
from app.instances import tracks_instance
from app.lib.albumslib import create_album
from app.lib.albumslib import find_album
from app.lib.taglib import get_tags
from app.lib.trackslib import find_track
from app.logger import Log
from app.models import Album
from tqdm import tqdm

from app import instances


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
        self.tracks = []

    def run(self):
        self.check_untagged()
        self.tag_untagged()

        if len(self.tagged_tracks) == 0:
            return

        # self.tagged_tracks.sort(key=lambda x: x["albumhash"])

        self.pre_albums = self.create_pre_albums(self.tagged_tracks)
        self.create_albums(self.pre_albums)

        self.albums.sort(key=lambda x: x.hash)
        self.create_tracks()

        self.save_all()

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

    def get_tags(self, file: str):
        tags = get_tags(file)

        if tags is not None:
            hash = create_album_hash(tags["album"], tags["albumartist"])
            tags["albumhash"] = hash
            self.tagged_tracks.append(tags)

    def tag_untagged(self):
        """
        Loops through all the untagged files and tags them.
        """

        s = time.time()
        print(f"Started tagging files")
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_tags, self.files)

        tracks_instance.insert_many(self.tagged_tracks)
        d = time.time() - s
        Log(f"Tagged {len(self.tagged_tracks)} files in {d} seconds")

    @staticmethod
    def create_pre_albums(tracks: List[dict]):
        """
        Creates pre-albums for the all tagged tracks.
        """
        prealbums = []

        for track in tqdm(tracks, desc="Creating pre-albums"):
            album = {"title": track["album"], "artist": track["albumartist"]}

            if album not in prealbums:
                prealbums.append(album)

        Log(f"Created {len(prealbums)} pre-albums")
        return prealbums

    def create_album(self, album: dict):
        albumhash = create_album_hash(album["title"], album["artist"])
        album = instances.album_instance.find_album_by_hash(albumhash)

        if album is not None:
            self.albums.append(album)
            self.exist_count += 1
            return

        index = find_track(self.tagged_tracks, albumhash)

        track = self.tagged_tracks[index]

        album = create_album(track, self.tagged_tracks)

        if album is None:
            print("album is none")
            return

        album = Album(album)

        self.albums.append(album)

    def create_albums(self, albums: List[dict]):
        """
        Uses the pre-albums to create new albums and add them to the database.
        """
        for album in tqdm(albums, desc="Building albums"):
            self.create_album(album)

        Log(f"{self.exist_count} of {len(albums)} albums were already in the database")

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
        return track

    def create_tracks(self):
        """
        Loops through all the tagged tracks creating complete track objects using the `models.Track` model.
        """
        with ThreadPoolExecutor() as executor:
            iterable = executor.map(self.create_track, self.tagged_tracks)

            self.tracks = [t for t in iterable if t is not None]

        Log(
            f"Added {len(self.tagged_tracks)} new tracks and {len(self.albums)} new albums"
        )

    def save_all(self):
        """
        Saves the albums to the database.
        """

        album_instance.insert_many([a.__dict__ for a in self.albums])
        tracks_instance.insert_many(self.tracks)
