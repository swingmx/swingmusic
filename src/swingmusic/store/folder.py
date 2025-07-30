import pathlib

from sortedcontainers import SortedSet
from concurrent.futures import ThreadPoolExecutor

from swingmusic.db.libdata import TrackTable
from swingmusic.store.tracks import TrackStore


class FolderStore:
    """
    The Folder store is used to hold all the indexed tracks filepaths in memory
    for fast count operations when browsing the folder page.

    Counting from the database is super slow,
    even with a small number of folders to get the count for Up to 700 ms for 10 folders.
    By using this store, we are able to reduce that to less than 10 ms.
    """

    filepaths: SortedSet = SortedSet()
    map: dict[str, str] = {}
    """
    The map above is a dictionary that maps the folder path to the track hash, which can be used to fetch the track from the track store (a dict of track hashes to track objects).
    """


    @classmethod
    def load_filepaths(cls):
        """
        Load all the filepaths from the database into memory.

        This is needed to speed up the process of counting the number of tracks in the folder page.
        """
        cls.filepaths.clear()

        tracks = TrackTable.get_all()
        for track in tracks:
            cls.filepaths.add(track.filepath)
            cls.map[track.filepath] = track.trackhash


    @classmethod
    def get_tracks_by_filepaths(cls, filepaths: list[str]):
        """
        Generator which tries to match TrackStore with track hash
        """
        for filepath in filepaths:
            filepath = pathlib.Path(filepath).as_posix()

            if filepath in cls.map:
                trackhash = cls.map[filepath]
                trackgroup = TrackStore.trackhashmap.get(trackhash)

                if trackgroup is None:
                    continue

                for track in trackgroup.tracks:
                    if track.filepath == filepath:
                        yield track


    @classmethod
    def count_tracks_containing_paths(cls, paths: list[str]):
        """
        Count the number of tracks in each directory.

        Uses a ThreadPoolExecutor to count the number of tracks
        in each directory for fast execution time.
        """

        with ThreadPoolExecutor() as executor:
            res = executor.map(count_filepaths_in_dir, ((path, FolderStore.filepaths) for path in paths))
            results = [
                {"path": path, "trackcount": count} for path, count in zip(paths, res)
            ]

        return results


def get_index_of_first_match(paths: list[str], prefix: str) -> int:
    """
    Find index of first match.
    Uses binary search to speed up the search process.

    :params paths: List of string to march.
    :params prefix: Prefix to match against with `startswith`.
    :returns: -1 if no element found, 0 if everything matches, else result > 0
    """

    left = 0
    right = len(paths) - 1

    while left <= right:
        mid = (left + right) // 2

        if paths[mid].startswith(prefix):
            if mid == 0 or not paths[mid - 1].startswith(prefix):
                return mid
            right = mid - 1

        elif paths[mid] < prefix:
            left = mid + 1

        else:
            right = mid - 1

    return -1


def count_filepaths_in_dir(_map: tuple[str, SortedSet]):
    """
    Counts the number of filepaths that start with the given directory path.

    Gets the index of the first path that starts with the given directory path,
    then check each path after that to see if it starts with the given directory path.
    """
    dirpath, filepaths = _map
    index = get_index_of_first_match(filepaths, dirpath)

    count = 0

    for path in filepaths[index:]:
        if path.startswith(dirpath):
            count += 1
        else:
            break

    return count
