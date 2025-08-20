import os
from functools import partial
from multiprocessing import Pool, cpu_count

from swingmusic import settings
from swingmusic.config import UserConfig
from swingmusic.db.libdata import TrackTable

from swingmusic.lib.taglib import extract_thumb, get_tags
from swingmusic.models.album import Album
from swingmusic.models.artist import Artist
from swingmusic.models.track import Track
from swingmusic.store.folder import FolderStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils import flatten
from swingmusic.utils.filesystem import run_fast_scandir
from swingmusic.utils.parsers import get_base_album_title
from swingmusic.utils.progressbar import tqdm
from swingmusic.utils.remove_duplicates import remove_duplicates


from logging import getLogger
log = getLogger(__name__)


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

        try:
            if dirs_to_scan[0] == "$home":
                dirs_to_scan = [settings.Paths().USER_HOME_DIR.as_posix()]
        except IndexError:
            pass

        files = set()

        for _dir in dirs_to_scan:
            files = files.union(run_fast_scandir(_dir, full=True)[1])

        unmodified, modified_tracks = self.filter_modded()
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
                    track["filepath"], track["albumhash"] + ".webp", overwrite=True, paths=settings.Paths()
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
                    "albumhash": track.albumhash,
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


    def tag_untagged(self, files: set[str]):
        config = UserConfig()

        # Create process pool with worker function
        with Pool(processes=max(1, cpu_count() // 2)) as pool:
            worker = partial(parse_file_tags, config=config)

            # Process files and track progress
            results = []
            for result in tqdm(
                pool.imap_unordered(worker, files),
                total=len(files),
                desc="Reading files",
            ):
                if result is not None:
                    results.append(result)

        # Bulk insert results
        for tags in results:
            TrackTable.insert_one(tags)
            FolderStore.filepaths.add(tags["filepath"])

        print(f"{len(results)} new files indexed")
        print("Done")



#
# Create functions
#

def create_albums(_trackhashes: list[str] = []) -> list[tuple[Album, set[str]]]:
    """
    Creates album objects using the indexed tracks. Takes in an optional
    list of trackhashes to create the albums from. If no list is provided,
    all tracks are used.

    The trackhashes are passed when creating albums from the watchdogg module.

    Returns a list of tuples containing the album and the trackhashes in the album.
    ie:

    >>> list[tuple[Album, set[str]]]
    """
    albums = dict()

    if _trackhashes:
        all_tracks: list[Track] = TrackStore.get_tracks_by_trackhashes(_trackhashes)
    else:
        all_tracks: list[Track] = TrackStore.get_flat_list()

    all_tracks = remove_duplicates(all_tracks)

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
                "tracks": {track.trackhash},
                "pathhash": track.pathhash,
                "extra": {},
            }
        else:
            album = albums[track.albumhash]
            album["tracks"].add(track.trackhash)
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
        album["genrehashes"] = " ".join([g["genrehash"] for g in genres])
        album["base_title"], _ = get_base_album_title(album["og_title"])

        del genres
        trackhashes = album.pop("tracks")
        album["trackcount"] = len(trackhashes)

        albums[album["albumhash"]] = (Album(**album), trackhashes)

    return list(albums.values())


def create_artists( artisthashes: list[str]) -> list[tuple[Artist, set[str], set[str]]]:
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
                    "lastplayed": track.lastplayed,
                    "playcount": track.playcount,
                    "playduration": track.playduration,
                    "trackcount": None,
                    "tracks": (
                        {track.trackhash} if thisartist.get("in_track", True) else set()
                    ),
                    "extra": {},
                }
            else:
                artist: dict = artists[thisartist["artisthash"]]
                artist["duration"] += track.duration
                artist["playcount"] += track.playcount
                artist["playduration"] += track.playduration
                artist["albums"].add(track.albumhash)
                artist["date"] = min(artist["date"], track.date)
                artist["lastplayed"] = max(artist["lastplayed"], track.lastplayed)
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
        artist["name"] = sorted(artist["names"])[0]

        # INFO: Delete temporary keys
        del artist["names"]

        tracks = artist.pop("tracks")
        albums = artist.pop("albums")

        # INFO: Delete local variables
        del genres

        artists[artist["artisthash"]] = (Artist(**artist), tracks, albums)

    return list(artists.values())
