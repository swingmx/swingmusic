import os
import posixpath
import urllib.parse
from pathlib import Path

from natsort import natsorted

from swingmusic.lib.sortlib import sort_tracks
from swingmusic.models.track import Track
from swingmusic.utils.filesystem import is_hidden_file

PLAYLIST_EXTENSIONS = (".m3u", ".m3u8")


def pick_playlist(folder: Path, playlists: list[str]) -> str | None:
    """
    Returns the playlist named like `folder`, else the first in natural order.
    """
    if not playlists:
        return None

    for playlist in playlists:
        if Path(playlist).stem.casefold() == folder.name.casefold():
            return playlist

    return natsorted(playlists)[0]


def folder_playlist(folder: Path) -> str | None:
    """
    Returns the m3u playlist that orders `folder`, if it has one.
    """
    try:
        playlists = [
            entry.as_posix()
            for entry in folder.iterdir()
            if entry.suffix.lower() in PLAYLIST_EXTENSIONS
            and not is_hidden_file(entry.name)
            and entry.is_file()
        ]
    except OSError:
        return None

    return pick_playlist(folder, playlists)


def read_m3u(path: str) -> list[str]:
    """
    Returns the resolved file paths listed in an m3u playlist, in order.
    """
    playlist = Path(path)

    try:
        raw = playlist.read_bytes()
    except OSError:
        return []

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")

    entries: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if line.lower().startswith("file://"):
            line = urllib.parse.unquote(urllib.parse.urlsplit(line).path)

        entry = Path(line.replace("\\", "/"))
        if not entry.is_absolute():
            entry = playlist.parent / entry

        try:
            entries.append(entry.resolve().as_posix())
        except (OSError, RuntimeError, ValueError):
            continue

    return entries


def sort_by_m3u(tracks: list[Track], entries: list[str]) -> list[Track]:
    """
    Orders tracks by their first position in `entries`, matching full paths then filenames.
    Unlisted tracks go last, in their given order.
    """
    by_path: dict[str, int] = {}
    by_name: dict[str, int] = {}

    for index, entry in enumerate(entries):
        by_path.setdefault(entry, index)
        by_name.setdefault(posixpath.basename(entry).casefold(), index)

    def position(track: Track) -> int:
        if track.filepath in by_path:
            return by_path[track.filepath]

        return by_name.get(os.path.basename(track.filepath).casefold(), len(entries))

    return sorted(tracks, key=position)


def sort_by_folder_playlist(tracks: list[Track], playlist: str, reverse: bool) -> list[Track]:
    """
    Orders tracks by `playlist`, unlisted tracks last in default order.
    """
    tracks = sort_by_m3u(sort_tracks(tracks, "default"), read_m3u(playlist))
    return tracks[::-1] if reverse else tracks


def sort_folder_tracks(tracks: list[Track], folder: Path, sortby: str, reverse: bool) -> list[Track]:
    """
    Sorts tracks from `folder`, following its m3u playlist for the default sort.
    """
    playlist = folder_playlist(folder) if sortby == "default" else None
    if playlist is None:
        return sort_tracks(tracks, sortby, reverse)

    return sort_by_folder_playlist(tracks, playlist, reverse)
