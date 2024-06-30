import gc
import os
from pprint import pprint
from time import time
from typing import Generator
from app import settings
from app.config import UserConfig
from app.db.libdata import ArtistTable
from app.db.libdata import AlbumTable, TrackTable
from app.lib.populate import CordinateMedia
from app.lib.taglib import extract_thumb, get_tags
from app.models.track import Track
from app.store.folder import FolderStore
from app.utils.filesystem import run_fast_scandir
from app.utils.parsers import get_base_album_title
from app.utils.progressbar import tqdm

from app.logger import log
from app.utils.threading import background

POPULATE_KEY: float = 0


class IndexTracks:
    def __init__(self, instance_key: float) -> None:
        """
        Indexes all tracks in the database.

        An instance key is used to prevent multiple instances of the
        same class from running at the same time.
        """
        global POPULATE_KEY
        POPULATE_KEY = instance_key

        # dirs_to_scan = sdb.get_root_dirs()
        dirs_to_scan = UserConfig().rootDirs

        if len(dirs_to_scan) == 0:
            log.warning(
                (
                    "The root directory is not configured. "
                    + "Open the app in your webbrowser to configure."
                )
            )
            return

        try:
            if dirs_to_scan[0] == "$home":
                dirs_to_scan = [settings.Paths.USER_HOME_DIR]
        except IndexError:
            pass

        files = set()

        for _dir in dirs_to_scan:
            files = files.union(run_fast_scandir(_dir, full=True)[1])

        unmodified, modified_tracks = self.filter_modded()
        untagged = files - unmodified

        self.tag_untagged(untagged, instance_key)
        self.extract_thumb_with_overwrite(modified_tracks)

    @staticmethod
    def extract_thumb_with_overwrite(tracks: list[dict[str, str]]):
        """
        Extracts the thumbnail from a list of filepaths,
        overwriting the existing thumbnail if it exists,
        for modified files.
        """
        for track in tracks:
            try:
                extract_thumb(
                    track["filepath"], track["trackhash"] + ".webp", overwrite=True
                )
            except FileNotFoundError:
                continue

    @staticmethod
    def filter_modded():
        """
        Removes tracks from the database that have been modified
        since they were indexed.

        Returns a tuple of unmodified paths and modified tracks.
        Unmodified paths are indexed and the modified tracks are

        """

        unmodified_paths = set()
        modified_tracks: list[dict[str, str]] = []

        to_remove = set()

        for track in TrackTable.get_all():
            try:
                if track.last_mod == round(os.path.getmtime(track.filepath)):
                    unmodified_paths.add(track.filepath)
                    continue
            except (FileNotFoundError, OSError) as e:
                log.warning(e)  # REVIEW More informations = good
                to_remove.add(track.filepath)

            modified_tracks.append(
                {
                    "filepath": track.filepath,
                    "trackhash": track.trackhash,
                }
            )

        to_remove = to_remove.union(set(t["filepath"] for t in modified_tracks))
        TrackTable.remove_tracks_by_filepaths(to_remove)

        # REVIEW: Remove after testing!
        track = TrackTable.get_tracks_by_filepaths(list(to_remove)[:1])
        if track:
            raise Exception("Track not removed")
        # =============================================================

        return unmodified_paths, modified_tracks

    def get_untagged(self):
        tracks = TrackTable.get_all()

    def tag_untagged(self, files: set[str], key: float):
        config = UserConfig()
        for file in tqdm(files, desc="Reading files"):
            if POPULATE_KEY != key:
                log.warning("'Populate.tag_untagged': Populate key changed")
                return

            tags = get_tags(file, artist_separators=config.artistSeparators)

            if tags is not None:
                TrackTable.insert_one(tags)
                FolderStore.filepaths.add(tags["filepath"])

            del tags

        print(f"{len(files)} new files indexed")
        print("Done")


class IndexAlbums:
    def __init__(self) -> None:
        albums = dict()
        all_tracks: list[Track] = TrackTable.get_all()

        if len(all_tracks) == 0:
            return

        for track in all_tracks:
            if track.albumhash not in albums:
                albums[track.albumhash] = {
                    "albumartists": track.albumartists,
                    "artisthashes": [a["artisthash"] for a in track.albumartists],
                    "albumhash": track.albumhash,
                    "base_title": None,
                    "color": None,
                    "created_date": track.last_mod,
                    "date": track.date,
                    "duration": track.duration,
                    "genres": [*track.genres] if track.genres else [],
                    "og_title": track.og_album,
                    "lastplayed": track.lastplayed,
                    "playcount": track.playcount,
                    "playduration": track.playduration,
                    "title": track.album,
                    "trackcount": 1,
                }
            else:
                album = albums[track.albumhash]
                album["trackcount"] += 1
                album["playcount"] += track.playcount
                album["playduration"] += track.playduration
                album["lastplayed"] = max(album["lastplayed"], track.lastplayed)
                album["duration"] += track.duration
                album["date"] = min(album["date"], track.date)
                album["created_date"] = min(album["created_date"], track.last_mod)

                if track.genres:
                    album["genres"].extend(track.genres)

        for album in albums.values():
            genres = []
            for genre in album["genres"]:
                if genre not in genres:
                    genres.append(genre)

            album["genres"] = genres
            album["base_title"], _ = get_base_album_title(album["og_title"])

            del genres

        AlbumTable.remove_all()
        AlbumTable.insert_many(list(albums.values()))
        del albums


class IndexArtists:
    def __init__(self) -> None:
        all_tracks: list[Track] = TrackTable.get_all()
        artists = dict()

        if len(all_tracks) == 0:
            return

        for track in all_tracks:
            this_artists = track.artists

            for a in track.albumartists:
                if a not in this_artists:
                    this_artists.append(a)

            for thisartist in this_artists:
                if thisartist["artisthash"] not in artists:
                    artists[thisartist["artisthash"]] = {
                        "albumcount": None,
                        "albums": {track.albumhash},
                        "artisthash": thisartist["artisthash"],
                        "created_date": track.last_mod,
                        "date": track.date,
                        "duration": track.duration,
                        "genres": track.genres if track.genres else [],
                        "name": None,
                        "names": {thisartist["name"]},
                        "lastplayed": track.lastplayed,
                        "playcount": track.playcount,
                        "playduration": track.playduration,
                        "trackcount": None,
                        "tracks": {track.trackhash},
                    }
                else:
                    artist = artists[thisartist["artisthash"]]
                    artist["duration"] += track.duration
                    artist["playcount"] += track.playcount
                    artist["playduration"] += track.playduration
                    artist["albums"].add(track.albumhash)
                    artist["tracks"].add(track.trackhash)
                    artist["date"] = min(artist["date"], track.date)
                    artist["lastplayed"] = max(artist["lastplayed"], track.lastplayed)
                    artist["created_date"] = min(artist["created_date"], track.last_mod)
                    artist["names"].add(thisartist["name"])

                    if track.genres:
                        artist["genres"].extend(track.genres)

        for artist in artists.values():
            artist["albumcount"] = len(artist["albums"])
            artist["trackcount"] = len(artist["tracks"])

            genres = []

            for genre in artist["genres"]:
                if genre not in genres:
                    genres.append(genre)

            artist["genres"] = genres
            artist["name"] = sorted(artist["names"])[0]

            # INFO: Delete temporary keys
            del artist["names"]
            del artist["tracks"]
            del artist["albums"]

            # INFO: Delete local variables
            del genres

        ArtistTable.remove_all()
        ArtistTable.insert_many(list(artists.values()))
        del artists


class IndexEverything:
    def __init__(self) -> None:
        IndexTracks(instance_key=time())
        IndexAlbums()
        IndexArtists()
        FolderStore.load_filepaths()

        # pass

        CordinateMedia(instance_key=str(time()))
        gc.collect()


@background
def index_everything():
    return IndexEverything()
