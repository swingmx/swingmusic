# from tqdm import tqdm

import itertools
import json
from typing import Callable, Iterable
from swingmusic.db.libdata import TrackTable

from swingmusic.models import Track
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.remove_duplicates import remove_duplicates

TRACKS_LOAD_KEY = ""


class TrackGroup:
    """
    Tracks grouped under the same trackhash.
    """

    def __init__(self, tracks: list[Track]):
        self.tracks = tracks

    def append(self, track: Track):
        """
        Adds a track to the group.
        """
        self.tracks.append(track)

    def remove(self, track: Track):
        """
        Removes a track from the group.
        """
        self.tracks.remove(track)

    def increment_playcount(self, duration: int, timestamp: int, playcount: int = 1):
        """
        Increments the playcount of all tracks in the group.
        """
        for track in self.tracks:
            track.playcount += playcount
            track.lastplayed = timestamp
            track.playduration += duration

    def toggle_favorite_user(self, userid: int | None = None):
        """
        Adds or removes a user from the list of users who have favorited the track.
        """
        if userid is None:
            userid = get_current_userid()

        for track in self.tracks:
            track.toggle_favorite_user(userid)

    def get_best(self):
        """
        Returns the track with higest bitrate.
        """
        return max(self.tracks, key=lambda x: x.bitrate)

    def __len__(self):
        return len(self.tracks)


class classproperty(property):
    """
    A class property decorator.
    """

    def __get__(self, owner_self, owner_cls):
        if self.fget:
            return self.fget(owner_cls)


class TrackStore:
    # {'trackhash': Track[]}
    trackhashmap: dict[str, TrackGroup] = dict()

    @classproperty
    def tracks(cls) -> list[Track]:
        return cls.get_flat_list()

    @classmethod
    def get_flat_list(cls):
        """
        Returns a flat list of all tracks.
        """
        return list(
            itertools.chain.from_iterable(
                [group.tracks for group in cls.trackhashmap.values()]
            )
        )

    @classmethod
    def load_all_tracks(cls, instance_key: str):
        """
        Loads all tracks from the database into the store.
        """

        print("Loading tracks... ", end="")
        global TRACKS_LOAD_KEY
        TRACKS_LOAD_KEY = instance_key

        cls.trackhashmap = dict()
        tracks = TrackTable.get_all()

        # INFO: Load all tracks into the dict store
        for track in tracks:
            if instance_key != TRACKS_LOAD_KEY:
                return

            exists = cls.trackhashmap.get(track.trackhash, None)
            if not exists:
                cls.trackhashmap[track.trackhash] = TrackGroup([track])
            else:
                cls.trackhashmap[track.trackhash].append(track)

        print("Done!")

    @classmethod
    def add_track(cls, track: Track):
        """
        Adds a single track to the store.
        """
        group = cls.trackhashmap.get(track.trackhash, None)

        if group:
            return group.append(track)

        cls.trackhashmap[track.trackhash] = TrackGroup([track])

    @classmethod
    def add_tracks(cls, tracks: list[Track]):
        """
        Adds multiple tracks to the store.
        """

        for track in tracks:
            cls.add_track(track)

    @classmethod
    def remove_track(cls, track: Track):
        """
        Removes a single track from the store.
        """
        group = cls.trackhashmap.get(track.trackhash, None)

        if group:
            group.remove(track)

            if len(group) == 0:
                del cls.trackhashmap[track.trackhash]

    @classmethod
    def remove_track_by_filepath(cls, filepath: str):
        """
        Removes a track from the store by its filepath.
        """

        return cls.remove_tracks_by_filepaths({filepath})

    @classmethod
    def remove_tracks_by_filepaths(cls, filepaths: set[str]):
        """
        Removes multiple tracks from the store by their filepaths.
        """

        filecount = len(filepaths)

        for trackhash in cls.trackhashmap:
            group = cls.trackhashmap[trackhash]

            for track in group.tracks:
                if track.filepath in filepaths:
                    group.remove(track)

                    if len(group) == 0:
                        del cls.trackhashmap[trackhash]

                    filecount -= 1

                if filecount == 0:
                    break

    @classmethod
    def count_tracks_by_trackhash(cls, trackhash: str) -> int:
        """
        Counts the number of tracks with a specific trackhash.
        """
        return len(cls.trackhashmap.get(trackhash, []))

    # ================================================
    # ================== GETTERS =====================
    # ================================================

    @classmethod
    def get_tracks_by_trackhashes(cls, trackhashes: Iterable[str]) -> list[Track]:
        """
        Returns a list of tracks by their hashes.
        """
        hash_set = set(trackhashes)

        tracks: list[Track] = []

        for trackhash in hash_set:
            group = cls.trackhashmap.get(trackhash, None)

            if group:
                track = group.get_best()
                tracks.append(track)

        # sort the tracks in the order of the given trackhashes
        if type(trackhashes) == list:
            tracks.sort(key=lambda t: trackhashes.index(t.trackhash))

        return tracks

    @classmethod
    def get_tracks_by_filepaths(cls, paths: list[str]) -> list[Track]:
        """
        Returns all tracks matching the given paths.
        """
        # tracks = sorted(cls.trackhashmap, key=lambda x: x.filepath)
        # tracks = use_bisection(tracks, "filepath", paths)
        # return [track for track in tracks if track is not None]
        # return cls.find_tracks_by(key="filepath", value=paths)

        tracks: list[Track] = []

        for trackhash in cls.trackhashmap:
            group = cls.trackhashmap.get(trackhash)

            if not group:
                continue

            for track in group.tracks:
                if track.filepath in paths:
                    tracks.append(track)

        return tracks

    @classmethod
    def find_tracks_by(
        cls,
        key: str,
        value: str,
        predicate: Callable = lambda prop_value, value: prop_value == value,
        including_duplicates: bool = False,
    ):
        """
        Find all tracks by a specific key.
        """
        tracks: list[Track] = []

        for trackhash in cls.trackhashmap:
            group = cls.trackhashmap.get(trackhash, None)

            if not group:
                continue

            for track in group.tracks:
                prop_value = getattr(track, key)
                if predicate(prop_value, value):
                    tracks.append(track)

        if including_duplicates:
            return tracks

        return remove_duplicates(tracks)

    @classmethod
    def get_tracks_by_albumhash(cls, album_hash: str) -> list[Track]:
        """
        Returns all tracks matching the given album hash.
        """
        return cls.find_tracks_by(key="albumhash", value=album_hash)

    @classmethod
    def get_tracks_by_artisthash(cls, artisthash: str):
        """
        Returns all tracks matching the given artist. Duplicate tracks are removed.
        """
        predicate = lambda artisthashes, artisthash: artisthash in artisthashes
        return cls.find_tracks_by(
            key="artisthashes", value=artisthash, predicate=predicate
        )

    @classmethod
    def get_tracks_in_path(cls, path: str):
        """
        Returns all tracks in the given path.
        """
        predicate: Callable[[str, str], bool] = (
            lambda track_folder, path: track_folder.startswith(path)
        )

        return cls.find_tracks_by(
            key="folder",
            value=path,
            predicate=predicate,
            including_duplicates=True,
        )

    @classmethod
    def get_recently_added(cls, start: int, limit: int | None):
        """
        Returns the most recently added tracks.
        """
        tracks = cls.get_flat_list()

        if limit is None:
            return sorted(tracks, key=lambda x: x.last_mod, reverse=True)[start:]

        return sorted(tracks, key=lambda x: x.last_mod, reverse=True)[start:limit]

    @classmethod
    def get_recently_played(cls, limit: int):
        tracks = cls.get_flat_list()
        return sorted(tracks, key=lambda x: x.lastplayed, reverse=True)[:limit]

    @classmethod
    def export(cls):
        path = "tracks.json"

        with open(path, "w") as f:
            data = [
                {
                    "title": t.title,
                    "album": t.album,
                    "artists": [a["name"] for a in t.artists],
                }
                for t in cls.get_flat_list()
            ]
            json.dump(data, f)
