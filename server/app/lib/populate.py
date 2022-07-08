import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List

from app import instances
from app import settings
from app.helpers import create_hash
from app.helpers import Get
from app.helpers import run_fast_scandir
from app.helpers import UseBisection
from app.instances import tracks_instance
from app.lib.albumslib import create_album
from app.lib.taglib import get_tags
from app.logger import logg
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
        self.db_tracks = []
        self.tagged_tracks = []

        self.files = run_fast_scandir(settings.HOME_DIR, full=True)[1]
        self.db_tracks = tracks_instance.get_all_tracks()

        self.check_untagged()
        self.tag_untagged()

    def check_untagged(self):
        """
        Loops through all the tracks in db tracks removing each
        from the list of tagged tracks if it exists.
        We will now only have untagged tracks left in `files`.
        """
        for track in tqdm(self.db_tracks, desc="Checking untagged"):
            if track["filepath"] in self.files:
                self.files.remove(track["filepath"])

    def get_tags(self, file: str):
        tags = get_tags(file)

        if tags is not None:
            hash = create_hash(tags["album"], tags["albumartist"])
            tags["albumhash"] = hash
            self.tagged_tracks.append(tags)

    def tag_untagged(self):
        """
        Loops through all the untagged files and tags them.
        """

        logg.info("Tagging untagged tracks...")
        with ThreadPoolExecutor() as executor:
            executor.map(self.get_tags, self.files)

        if len(self.tagged_tracks) > 0:
            tracks_instance.insert_many(self.tagged_tracks)

        logg.info(f"Tagged {len(self.tagged_tracks)} tracks.")


@dataclass
class PreAlbum:
    title: str
    artist: str
    hash: str


class CreateAlbums:

    def __init__(self) -> None:
        self.db_tracks = Get.get_all_tracks()
        self.db_albums = Get.get_all_albums()

        prealbums = self.create_pre_albums(self.db_tracks)
        prealbums = self.filter_processed(self.db_albums, prealbums)

        albums = []

        for album in tqdm(prealbums, desc="Creating albums"):
            a = self.create_album(album)
            if a is not None:
                albums.append(a)

        # with ThreadPoolExecutor() as pool:
        #     iterator = pool.map(self.create_album, prealbums)

        #     for i in iterator:
        #         if i is not None:
        #             albums.append(i)

        if len(albums) > 0:
            instances.album_instance.insert_many(albums)

    @staticmethod
    def create_pre_albums(tracks: List[Track]) -> List[PreAlbum]:
        prealbums = []

        for track in tqdm(tracks, desc="Creating prealbums"):
            album = {
                "title": track.album,
                "artist": track.albumartist,
                "hash": track.albumhash,
            }

            album = PreAlbum(**album)

            if album not in prealbums:
                prealbums.append(album)

        return prealbums

    @staticmethod
    def filter_processed(albums: List[Album],
                         prealbums: List[PreAlbum]) -> List[dict]:
        to_process = []

        for p in tqdm(prealbums, desc="Filtering processed albums"):
            album = UseBisection(albums, "hash", [p.hash])()[0]

            if album is None:
                to_process.append(p)

        return to_process

    def create_album(self, album: PreAlbum) -> Album:
        hash = album.hash

        album = {"image": None}
        iter = 0

        while album["image"] is None:
            track = UseBisection(self.db_tracks, "albumhash", [hash])()[0]

            if track is not None:
                iter += 1
                album = create_album(track)
                self.db_tracks.remove(track)
            else:
                album["image"] = hash + ".webp"
        try:
            album = Album(album)
            return album
        except KeyError:
            print(f"📌 {iter}")
            print(album)
