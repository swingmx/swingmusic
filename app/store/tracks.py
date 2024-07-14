# from tqdm import tqdm

import itertools
from typing import Callable, Iterable
from flask_jwt_extended import current_user
from app.db.libdata import TrackTable
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb

# from app.db.sqlite.tracks import SQLiteTrackMethods as trackdb
from app.db.userdata import FavoritesTable
from app.models import Track
from app.utils.remove_duplicates import remove_duplicates

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

    def set_fav_userids(self, userids: set[int]):
        """
        Sets the favorite userids.
        """
        for track in self.tracks:
            track.fav_userids = userids

    def get_best(self):
        """
        Returns the track with higest bitrate.
        """
        return max(self.tracks, key=lambda x: x.bitrate)

    def toggle_favorite(self, remove: bool = False):
        """
        Adds a track to the favorites.
        """

        userids = set(self.tracks[0].fav_userids)

        if remove:
            userids.remove(current_user["id"])
        else:
            userids.add(current_user["id"])

        for track in self.tracks:
            track.fav_userids = userids

    def __len__(self):
        return len(self.tracks)


class classproperty(property):
    """
    A class property decorator.
    """

    def __get__(self, owner_self, owner_cls):
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

        # favs = favdb.get_fav_tracks()
        favs = FavoritesTable.get_all()
        records: dict[str, set[int]] = dict()

        # convert records: {trackhash: {userid, userid, ...}}
        for fav in favs:
            if fav.hash not in records:
                # if trackhash not in dict, add it
                # and set the value to a set containing the userid
                records[fav.hash] = {fav.userid}

            # if trackhash is in dict, add the userid to the set
            records[fav.hash].add(fav.userid)

        for record in records:
            if instance_key != TRACKS_LOAD_KEY:
                return

            group = cls.trackhashmap.get(record, None)

            if not group:
                continue

            group.set_fav_userids(records.get(record, set()))

        # print("Done!")
        # print(cls.trackhashmap.get("0d6b22c19c").tracks[0].fav_userids)
        # sys.exit(0)

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

    @classmethod
    def toggle_favorite(cls, trackhash: str, remove: bool = False):
        """
        Adds a track to the favorites.
        """

        group = cls.trackhashmap.get(trackhash)

        if group:
            group.toggle_favorite(remove=remove)

    @classmethod
    def remove_track_from_fav(cls, trackhash: str):
        """
        Removes a track from the favorites.
        """
        return cls.toggle_favorite(trackhash, remove=True)

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

        ⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔⛔
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
            key="artist_hashes", value=artisthash, predicate=predicate
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
