from tqdm import tqdm

from app.models import Track
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.utils.bisection import UseBisection
from app.utils.remove_duplicates import remove_duplicates


class TrackStore:
    tracks: list[Track] = []

    @classmethod
    def load_all_tracks(cls):
        """
        Loads all tracks from the database into the store.
        """

        cls.tracks = list(tdb.get_all_tracks())

        fav_hashes = favdb.get_fav_tracks()
        fav_hashes = " ".join([t[1] for t in fav_hashes])

        for track in tqdm(cls.tracks, desc="Loading tracks"):
            if track.trackhash in fav_hashes:
                track.is_favorite = True

    @classmethod
    def add_track(cls, track: Track):
        """
        Adds a single track to the store.
        """

        cls.tracks.append(track)

    @classmethod
    def add_tracks(cls, tracks: list[Track]):
        """
        Adds multiple tracks to the store.
        """

        cls.tracks.extend(tracks)

    @classmethod
    def remove_track_by_filepath(cls, filepath: str):
        """
        Removes a track from the store by its filepath.
        """

        for track in cls.tracks:
            if track.filepath == filepath:
                cls.tracks.remove(track)
                break

    @classmethod
    def remove_tracks_by_dir_except(cls, dirs: list[str]):
        """Removes all tracks not in the root directories."""
        to_remove = set()

        for track in cls.tracks:
            if not track.folder.startswith(tuple(dirs)):
                to_remove.add(track.folder)

        tdb.remove_tracks_by_folders(to_remove)

    @classmethod
    def count_tracks_by_hash(cls, trackhash: str) -> int:
        """
        Counts the number of tracks with a specific hash.
        """

        count = 0

        for track in cls.tracks:
            if track.trackhash == trackhash:
                count += 1

        return count

    @classmethod
    def make_track_fav(cls, trackhash: str):
        """
        Adds a track to the favorites.
        """

        for track in cls.tracks:
            if track.trackhash == trackhash:
                track.is_favorite = True

    @classmethod
    def remove_track_from_fav(cls, trackhash: str):
        """
        Removes a track from the favorites.
        """

        for track in cls.tracks:
            if track.trackhash == trackhash:
                track.is_favorite = False

    @classmethod
    def append_track_artists(cls, albumhash: str, artists: list[str], new_album_title:str):
        tracks = cls.get_tracks_by_albumhash(albumhash)

        for track in tracks:
            track.add_artists(artists, new_album_title)

    # ================================================
    # ================== GETTERS =====================
    # ================================================

    @classmethod
    def get_tracks_by_trackhashes(cls, trackhashes: list[str]) -> list[Track]:
        """
        Returns a list of tracks by their hashes.
        """

        trackhashes = " ".join(trackhashes)
        tracks = [track for track in cls.tracks if track.trackhash in trackhashes]

        tracks.sort(key=lambda t: trackhashes.index(t.trackhash))
        return tracks

    @classmethod
    def get_tracks_by_filepaths(cls, paths: list[str]) -> list[Track]:
        """
        Returns all tracks matching the given paths.
        """
        tracks = sorted(cls.tracks, key=lambda x: x.filepath)
        tracks = UseBisection(tracks, "filepath", paths)()
        return [track for track in tracks if track is not None]

    @classmethod
    def get_tracks_by_albumhash(cls, album_hash: str) -> list[Track]:
        """
        Returns all tracks matching the given album hash.
        """
        tracks = [t for t in cls.tracks if t.albumhash == album_hash]
        return remove_duplicates(tracks)

    @classmethod
    def get_tracks_by_artist(cls, artisthash: str) -> list[Track]:
        """
        Returns all tracks matching the given artist. Duplicate tracks are removed.
        """
        tracks = [t for t in cls.tracks if artisthash in t.artist_hashes]
        return remove_duplicates(tracks)
