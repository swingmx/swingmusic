import os
from contextlib import nullcontext
from functools import partial
from multiprocessing import Pool, cpu_count
import math

from natsort import natsorted

from swingmusic import settings
from swingmusic.config import UserConfig
from swingmusic.db.libdata import TrackTable
from swingmusic.events import events

from swingmusic.lib.taglib import extract_thumb, get_tags
from swingmusic.models.artist import Artist
from swingmusic.models.track import Track
from swingmusic.store.folder import FolderStore
from swingmusic.store.general import GeneralStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils import flatten
from swingmusic.utils.filesystem import is_hidden_file, run_fast_scandir
from swingmusic.utils.progressbar import tqdm
from swingmusic.utils.remove_duplicates import remove_duplicates


from logging import getLogger

log = getLogger(__name__)

# INFO: Batches up to this size are parsed in-process
INLINE_PARSE_LIMIT = 32


def resolve_root_dirs(root_dirs: list[str]) -> list[str]:
    """
    Expand the home placeholder into the user's home directory.
    """
    if root_dirs and root_dirs[0] == "$home":
        return [settings.Paths().USER_HOME_DIR.as_posix()]
    return list(root_dirs)


def root_prefixes(root_dirs: list[str]) -> tuple[str, ...]:
    """
    Returns the resolved root directories, each ending with a path separator.
    """
    return tuple(os.path.join(os.path.realpath(root), "") for root in root_dirs)


def is_under_roots(filepath: str, root_dirs: list[str]) -> bool:
    """
    Whether a file path lives inside one of the root directories.
    """
    return filepath.startswith(root_prefixes(root_dirs))


def parse_file_tags(file: str, config: UserConfig) -> dict | None:
    """Worker function to process individual files"""
    try:
        return get_tags(file, config=config)
    except Exception as e:
        log.warning(f"Failed to process file {file}: {e}")
        return None


class IndexTracks:
    def __init__(self) -> None:
        """
        Indexes all tracks in the database.

        An instance key is used to prevent multiple instances of the
        same class from running at the same time.
        """
        dirs_to_scan = UserConfig().rootDirs

        if len(dirs_to_scan) == 0:
            log.warning(
                (
                    "The root directory is not configured. "
                    + "Open the app in your webbrowser to configure."
                )
            )
            return

        dirs_to_scan = resolve_root_dirs(dirs_to_scan)

        files = set()

        for _dir in dirs_to_scan:
            files = files.union(run_fast_scandir(_dir, full=True)[1])

        unmodified, modified_tracks = self.filter_modded(dirs_to_scan)
        untagged = files - unmodified

        self.tag_untagged(untagged)
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
                    track["filepath"],
                    track["albumhash"] + ".webp",
                    overwrite=True,
                    paths=settings.Paths(),
                )
            except FileNotFoundError:
                continue

    @staticmethod
    def filter_modded(root_dirs: list[str]):
        """
        Removes tracks from the database that are hidden, outside the root
        directories, missing, or modified since they were indexed.
        Returns a tuple of unmodified paths and modified tracks.

        Reads the indexed tracks from the in-memory track store.
        """

        unmodified_paths = set()
        modified_tracks: list[dict[str, str]] = []

        to_remove = set()
        prefixes = root_prefixes(root_dirs)

        for track in TrackStore.get_flat_list():
            if is_hidden_file(os.path.basename(track.filepath)) or not track.filepath.startswith(
                prefixes
            ):
                to_remove.add(track.filepath)
                continue

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
                    "albumhash": track.albumhash,
                }
            )

        to_remove = to_remove.union(set(t["filepath"] for t in modified_tracks))
        if to_remove:
            TrackTable.remove_tracks_by_filepaths(to_remove)

        return unmodified_paths, modified_tracks

    def tag_untagged(self, files: set[str]):
        if not files:
            print("No files to process")
            return

        config = UserConfig()
        batch_size = 150

        # Convert set to list for batching
        files_list = list(files)
        total_files = len(files_list)
        batches = math.ceil(total_files / batch_size)

        # Create process pool with worker function
        total_processed = 0

        events.dispatch(
            "scan_batch_cleared",
            {
                "batch": f"0/{batches}",
            },
        )
        GeneralStore.scan_message = "scan_batch_cleared: " + f"0/{batches}"

        use_pool = total_files > INLINE_PARSE_LIMIT

        with Pool(processes=max(1, cpu_count() // 2)) if use_pool else nullcontext() as pool:
            worker = partial(parse_file_tags, config=config)
            mapper = pool.imap_unordered if use_pool else map

            for batch_num in range(batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, total_files)
                batch_files = files_list[start_idx:end_idx]

                if not batch_files:
                    break

                # Process current batch
                batch_results = []
                for result in tqdm(
                    mapper(worker, batch_files),
                    total=len(batch_files),
                    desc=f"Batch {batch_num + 1}/{batches}",
                ):
                    if result is not None:
                        batch_results.append(result)

                # Bulk insert batch results
                for tags in batch_results:
                    TrackTable.insert_one(tags)
                    FolderStore.filepaths.add(tags["filepath"])

                total_processed += len(batch_results)

                # Dispatch event for batch completion
                events.dispatch(
                    "scan_batch_cleared",
                    {
                        "batch": f"{batch_num + 1}/{batches}",
                    },
                )
                GeneralStore.scan_message = (
                    "scan_batch_cleared: " + f"{batch_num + 1}/{batches}"
                )

                print(
                    f"Completed batch {batch_num + 1}/{batches}: {len(batch_results)} files indexed"
                )

        print(f"{total_processed} new files indexed")
        print("Done")


#
# Create functions
#


def create_artists(artisthashes: list[str]) -> list[tuple[Artist, set[str], set[str]]]:
    """
    Creates artist objects using the indexed tracks. Takes in an optional
    list of artisthashes to create the artists from. If no list is provided,
    all tracks are used.

    Returns a list of tuples containing the artist, the trackhashes for the artist
    and the albumhashes for the artist.
    ie:

    >>> list[tuple[Artist, set[str], set[str]]]
    """

    if artisthashes:
        all_tracks: list[Track] = flatten(
            [TrackStore.get_tracks_by_artisthash(hash) for hash in artisthashes]
        )
    else:
        all_tracks: list[Track] = TrackStore.get_flat_list()

    all_tracks = remove_duplicates(all_tracks)
    artists = dict()

    for track in all_tracks:
        this_artists = [*track.artists]

        for a in track.albumartists:
            if a not in this_artists:
                a["in_track"] = False
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
                    "trackcount": None,
                    "tracks": (
                        {track.trackhash} if thisartist.get("in_track", True) else set()
                    ),
                    "extra": {},
                }
            else:
                artist: dict = artists[thisartist["artisthash"]]
                artist["duration"] += track.duration
                artist["albums"].add(track.albumhash)
                artist["date"] = min(artist["date"], track.date)
                artist["created_date"] = min(artist["created_date"], track.last_mod)
                artist["names"].add(thisartist["name"])

                artist.setdefault("albums", set())

                if thisartist.get("in_track", True):
                    artist["tracks"].add(track.trackhash)

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
        artist["genrehashes"] = " ".join([g["genrehash"] for g in genres])
        artist["name"] = natsorted(artist["names"])[0]

        # INFO: Delete temporary keys
        del artist["names"]

        tracks = artist.pop("tracks")
        albums = artist.pop("albums")

        # INFO: Delete local variables
        del genres

        artists[artist["artisthash"]] = (Artist(**artist), tracks, albums)

    return list(artists.values())
