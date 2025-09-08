import pathlib
from pathlib import Path
import logging

from swingmusic.lib.sortlib import sort_folders, sort_tracks
from swingmusic.models import Folder
from swingmusic.serializers.track import serialize_tracks
from swingmusic.utils.filesystem import SUPPORTED_FILES
from swingmusic.store.folder import FolderStore

log = logging.getLogger(__name__)

def create_folder(path: str, trackcount=0) -> Folder:
    """
    Creates a folder object from a path.
    """
    folder = Path(path)

    return Folder(
        name=folder.name,
        path=folder.as_posix() + "/",
        is_sym=folder.is_symlink(),
        trackcount=trackcount,
    )


def get_folders(paths: list[str]) -> list:
    """
    Filters out folders that don't have any tracks and
    returns a list of folder objects.
    """
    folders = FolderStore.count_tracks_containing_paths(paths)
    return [
        create_folder(f["path"], f["trackcount"])
        for f in folders
        if f["trackcount"] > 0
    ]


def get_files_and_dirs(
    path: pathlib.Path,
    start: int,
    limit: int,
    tracksortby: str,
    foldersortby: str,
    tracksort_reverse: bool,
    foldersort_reverse: bool,
    tracks_only: bool = False,
    skip_empty_folders=True,
) -> dict[str: list|int|str]:
    """
    Scan folder for files and folders.
    Will only return files in `swingmusic.utils.filesystem.SUPPORTED_FILES`.
    If `skip_empty_folders` is True

    :param path:
    :param start:
    :param limit:
    :param tracksortby:
    :param foldersortby:
    :param tracksort_reverse:
    :param foldersort_reverse:
    :param tracks_only: If True, will only return tracks with no folders
    :param skip_empty_folders: If True, will call recursively and skip empty folders until >0 supported file found.
    :returns: List of tracks and folders in that immediate path.
    """

    path = pathlib.Path(path)

    # if file or non-existent
    if not path.exists() or not path.is_dir():
        return {
            "path": path.as_posix(),
            "tracks": [],
            "folders": [],
            "total": 0
        }


    # iter through all folders
    # add files with supported suffix
    # ignore hidden folder
    dirs, files = [], []
    for entry in path.iterdir():
        ext = entry.suffix.lower()

        if entry.is_dir() and not entry.stem.startswith("."):
            dirs.append((entry / "").as_posix())
            # only append as posix for FolderStore and sort_folder function
            # TODO: rework everything to support pathlib
            # add a trailing slash to the folder path
            # to avoid matching a folder starting with the same name as the root path
            # eg. .../Music and .../Music VideosI

        elif entry.is_file() and ext in SUPPORTED_FILES:
            files.append(entry)

    # sort files by most recent
    files_with_mtime = []
    for file in files:
        try:
            files_with_mtime.append(
                {
                    "path": file.as_posix(),
                    "time": file.lstat().st_mtime,
                }
            )
        except OSError as e:
            log.error(e)

    files_with_mtime.sort(key=lambda f: f["time"])
    files = [f["path"] for f in files_with_mtime]

    # if supported files were found
    # convert files to tracks
    tracks = []
    if len(files) > 0:
        if limit == -1:
            limit = len(files)

        # only return tracks already indexed by us
        tracks = list(FolderStore.get_tracks_by_filepaths(files))
        tracks = sort_tracks(tracks, tracksortby, tracksort_reverse)
        tracks = tracks[start : start + limit]


    folders = []
    if not tracks_only:
        folders = get_folders(dirs)
        folders = sort_folders(folders, foldersortby, foldersort_reverse)

    if skip_empty_folders and len(folders) == 1 and len(tracks) == 0:
        # INFO: When we only have one folder and no tracks,
        # skip through empty folders.
        # Call recursively with the first folder in the list.
        return get_files_and_dirs(
            folders[0].path,
            start=start,
            limit=limit,
            tracksortby=tracksortby,
            foldersortby=foldersortby,
            tracksort_reverse=tracksort_reverse,
            foldersort_reverse=foldersort_reverse,
            tracks_only=tracks_only,
            skip_empty_folders=True,
        )

    return {
        "path": path.as_posix(),
        "tracks": serialize_tracks(tracks),
        "folders": folders,
        "total": len(files),
    }
