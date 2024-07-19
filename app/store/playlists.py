from operator import index
from app.db.userdata import PlaylistTable
from app.lib.playlistlib import get_first_4_images
from app.models.playlist import Playlist
from app.store.tracks import TrackStore


class PlaylistEntry:
    def __init__(self, playlist: Playlist) -> None:
        self.playlist = playlist
        self.trackhashes: list[str] = playlist.trackhashes
        self.playlist.clear_lists()

        if not playlist.has_image:
            self.rebuild_images()

    def rebuild_images(self):
        self.playlist.images = get_first_4_images(
            TrackStore.get_tracks_by_trackhashes(self.trackhashes)
        )


class PlaylistStore:
    playlistmap: dict[str, PlaylistEntry] = {}

    @classmethod
    def load_playlists(cls):
        """
        Loads all playlists into the store.
        """
        cls.playlistmap = {str(p.id): PlaylistEntry(p) for p in PlaylistTable.get_all()}
        print(cls.playlistmap)

    @classmethod
    def get_playlist_tracks(cls, playlist_id: str, start: int, limit: int | None):
        """
        Returns the trackhashes for a playlist.
        """

        entry = cls.playlistmap.get(playlist_id)
        if entry is None:
            return []

        if limit is None:
            return TrackStore.get_tracks_by_trackhashes(entry.trackhashes[start:])

        return TrackStore.get_tracks_by_trackhashes(
            entry.trackhashes[start : start + limit]
        )

    @classmethod
    def get_flat_list(cls):
        return [p.playlist for p in cls.playlistmap.values()]

    @classmethod
    def add_playlist(cls, playlist: Playlist):
        cls.playlistmap[str(playlist.id)] = PlaylistEntry(playlist)

    @classmethod
    def get_playlist_by_id(cls, id: str):
        entry = cls.playlistmap.get(id)

        if entry is not None:
            return entry.playlist

    @classmethod
    def remove_from_playlist(cls, pid: str, tracks: list[dict[str, str]]):
        playlist = cls.playlistmap.get(pid)

        if not playlist:
            return

        for track in tracks:
            if playlist.trackhashes.index(track["trackhash"]) == track["index"]:
                playlist.trackhashes.remove(track["trackhash"])

        playlist.rebuild_images()
