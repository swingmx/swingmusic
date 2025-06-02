from sortedcontainers import SortedSet
from concurrent.futures import ThreadPoolExecutor

from swingmusic.db.libdata import TrackTable
from swingmusic.store.tracks import TrackStore


class FolderStore:
    """
    The Folder store is used to hold all the indexed tracks filepaths in memory
    for fast count operations when browsing the folder page.

    Counting from the database is super slow, even with a small number of folders to get the count for. Up to 700ms for 10 folders. By using this store, we are able to reduce that to less than 10ms.
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
        for filepath in filepaths:
            trackhash = cls.map.get(filepath)

            if trackhash:
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
        results: list[dict[str, int | str]] = []

        with ThreadPoolExecutor() as executor:
            res = executor.map(countFilepathsInDir, ((path, FolderStore.filepaths) for path in paths))
            results = [
                {"path": path, "trackcount": count} for path, count in zip(paths, res)
            ]

        return results


def getIndexOfFirstMatch(strings: list[str], prefix: str):
    """
    Find the index of the first path that starts with the given path.

    Uses a binary search algorithm to find the index.
    """

    left = 0
    right = len(strings) - 1

    while left <= right:
        mid = (left + right) // 2

        if strings[mid].startswith(prefix):
            if mid == 0 or not strings[mid - 1].startswith(prefix):
                return mid
            right = mid - 1
        elif strings[mid] < prefix:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def countFilepathsInDir(_map: tuple[str, SortedSet]):
    """
    Counts the number of filepaths that start with the given directory path.

    Gets the index of the first path that starts with the given directory path,
    then checks each path after that to see if it starts with the given directory path.
    """
    dirpath, filepaths = _map
    index = getIndexOfFirstMatch(filepaths, dirpath)

    if index == -1:
        return 0

    paths: list[str] = []

    for path in filepaths[index:]:
        if path.startswith(dirpath):
            paths.append(path)
        else:
            break

    return len(paths)
