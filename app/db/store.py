"""
In memory store.
"""
import json
import random
from pathlib import Path

from tqdm import tqdm

from app.db.sqlite.albums import SQLiteAlbumMethods as aldb
from app.db.sqlite.artists import SQLiteArtistMethods as ardb
from app.db.sqlite.favorite import SQLiteFavoriteMethods as favdb
from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.models import Album, Artist, Folder, Track
from app.utils import (
    UseBisection,
    create_folder_hash,
    get_all_artists,
    remove_duplicates,
)


class Store:
    """
    This class holds all tracks in memory and provides methods for
    interacting with them.
    """

    tracks: list[Track] = []
    folders: list[Folder] = []
    albums: list[Album] = []
    artists: list[Artist] = []

    @classmethod
    def load_all_tracks(cls):
        """
        Loads all tracks from the database into the store.
        """

        cls.tracks = list(tdb.get_all_tracks())

        fav_hashes = favdb.get_fav_tracks()
        fav_hashes = [t[1] for t in fav_hashes]

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
    def get_tracks_by_trackhashes(cls, trackhashes: list[str]) -> list[Track]:
        """
        Returns a list of tracks by their hashes.
        """

        tracks = []

        for trackhash in trackhashes:
            for track in cls.tracks:
                if track.trackhash == trackhash:
                    tracks.append(track)

        return tracks

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
    def count_tracks_by_hash(cls, trackhash: str) -> int:
        """
        Counts the number of tracks with a specific hash.
        """

        count = 0

        for track in cls.tracks:
            if track.trackhash == trackhash:
                count += 1

        return count

    # ====================================================
    # =================== FAVORITES ======================
    # ====================================================

    @classmethod
    def add_fav_track(cls, trackhash: str):
        """
        Adds a track to the favorites.
        """

        for track in cls.tracks:
            if track.trackhash == trackhash:
                track.is_favorite = True

    @classmethod
    def remove_fav_track(cls, trackhash: str):
        """
        Removes a track from the favorites.
        """

        for track in cls.tracks:
            if track.trackhash == trackhash:
                track.is_favorite = False

    # ====================================================
    # ==================== FOLDERS =======================
    # ====================================================

    @classmethod
    def check_has_tracks(cls, path: str):  # type: ignore
        """
        Checks if a folder has tracks.
        """
        path_hashes = "".join(f.path_hash for f in cls.folders)
        path_hash = create_folder_hash(*Path(path).parts[1:])

        return path_hash in path_hashes

    @classmethod
    def is_empty_folder(cls, path: str):
        """
        Checks if a folder has tracks using tracks in the store.
        """

        all_folders = set(track.folder for track in cls.tracks)
        folder_hashes = "".join(
            create_folder_hash(*Path(f).parts[1:]) for f in all_folders
        )

        path_hash = create_folder_hash(*Path(path).parts[1:])
        return path_hash in folder_hashes

    @staticmethod
    def create_folder(path: str) -> Folder:
        """
        Creates a folder object from a path.
        """
        folder = Path(path)

        return Folder(
            name=folder.name,
            path=str(folder),
            is_sym=folder.is_symlink(),
            has_tracks=True,
            path_hash=create_folder_hash(*folder.parts[1:]),
        )

    @classmethod
    def add_folder(cls, path: str):
        """
        Adds a folder to the store.
        """

        if cls.check_has_tracks(path):
            return

        folder = cls.create_folder(path)
        cls.folders.append(folder)

    @classmethod
    def remove_folder(cls, path: str):
        """
        Removes a folder from the store.
        """

        for folder in cls.folders:
            if folder.path == path:
                cls.folders.remove(folder)
                break

    @classmethod
    def process_folders(cls):
        """
        Creates a list of folders from the tracks in the store.
        """
        all_folders = [track.folder for track in cls.tracks]
        all_folders = set(all_folders)

        all_folders = [
            folder for folder in all_folders if not cls.check_has_tracks(folder)
        ]

        all_folders = [Path(f) for f in all_folders]
        all_folders = [f for f in all_folders if f.exists()]

        for path in tqdm(all_folders, desc="Processing folders"):
            folder = cls.create_folder(str(path))

            cls.folders.append(folder)

    @classmethod
    def get_folder(cls, path: str):  # type: ignore
        """
        Returns a folder object by its path.
        """
        folders = sorted(cls.folders, key=lambda x: x.path)
        folder = UseBisection(folders, "path", [path])()[0]

        if folder is not None:
            return folder

        has_tracks = cls.check_has_tracks(path)

        if not has_tracks:
            return None

        folder = cls.create_folder(path)
        cls.folders.append(folder)
        return folder

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
        return [t for t in cls.tracks if t.albumhash == album_hash]

    @classmethod
    def get_tracks_by_artist(cls, artisthash: str) -> list[Track]:
        """
        Returns all tracks matching the given artist. Duplicate tracks are removed.
        """
        tracks = [t for t in cls.tracks if artisthash in t.artist_hashes]
        return remove_duplicates(tracks)

    # ====================================================
    # ==================== ALBUMS ========================
    # ====================================================

    @staticmethod
    def create_album(track: Track):
        """
        Creates album object from a track
        """
        return Album(
            albumhash=track.albumhash,
            albumartists=track.albumartist,  # type: ignore
            title=track.album,
        )

    @classmethod
    def load_albums(cls):
        """
        Loads all albums from the database into the store.
        """

        albumhashes = set(t.albumhash for t in cls.tracks)

        for albumhash in tqdm(albumhashes, desc="Loading albums"):
            for track in cls.tracks:
                if track.albumhash == albumhash:
                    cls.albums.append(cls.create_album(track))
                    break

        db_albums: list[tuple] = aldb.get_all_albums()

        for album in tqdm(db_albums, desc="Mapping album colors"):
            albumhash = album[1]
            colors = json.loads(album[2])

            for al in cls.albums:
                if al.albumhash == albumhash:
                    al.set_colors(colors)
                    break

    @classmethod
    def add_album(cls, album: Album):
        """
        Adds an album to the store.
        """
        cls.albums.append(album)

    @classmethod
    def add_albums(cls, albums: list[Album]):
        """
        Adds multiple albums to the store.
        """
        cls.albums.extend(albums)

    @classmethod
    def get_albums_by_albumartist(
        cls, artisthash: str, limit: int, exclude: str
    ) -> list[Album]:
        """
        Returns N albums by the given albumartist, excluding the specified album.
        """

        albums = [
            album for album in cls.albums if artisthash in album.albumartisthash]

        albums = [album for album in albums if album.albumhash != exclude]

        if len(albums) > limit:
            random.shuffle(albums)

        # TODO: Merge this with `cls.get_albums_by_artisthash()`
        return albums[:limit]

    @classmethod
    def get_album_by_hash(cls, albumhash: str) -> Album | None:
        """
        Returns an album by its hash.
        """
        try:
            return [a for a in cls.albums if a.albumhash == albumhash][0]
        except IndexError:
            return None

    @classmethod
    def get_albums_by_artisthash(cls, artisthash: str) -> list[Album]:
        """
        Returns all albums by the given artist.
        """
        return [album for album in cls.albums if artisthash in album.albumartisthash]

    @classmethod
    def count_albums_by_artisthash(cls, artisthash: str):
        """
        Count albums for the given artisthash.
        """
        albumartists = [a.albumartists for a in cls.albums]
        artisthashes = []

        for artist in albumartists:
            artisthashes.extend([a.artisthash for a in artist])  # type: ignore

        master_string = "-".join(artisthashes)

        return master_string.count(artisthash)

    @classmethod
    def album_exists(cls, albumhash: str) -> bool:
        """
        Checks if an album exists.
        """
        return albumhash in "-".join([a.albumhash for a in cls.albums])

    @classmethod
    def remove_album_by_hash(cls, albumhash: str):
        """
        Removes an album from the store.
        """
        cls.albums = [a for a in cls.albums if a.albumhash != albumhash]

    # ====================================================
    # ==================== ARTISTS =======================
    # ====================================================

    @classmethod
    def load_artists(cls):
        """
        Loads all artists from the database into the store.
        """
        cls.artists = get_all_artists(cls.tracks, cls.albums)

        db_artists: list[tuple] = list(ardb.get_all_artists())

        for art in tqdm(db_artists, desc="Loading artists"):
            cls.map_artist_color(art)

    @classmethod
    def map_artist_color(cls, artist_tuple: tuple):
        """
        Maps a color to the corresponding artist.
        """

        artisthash = artist_tuple[1]
        color = json.loads(artist_tuple[2])

        for artist in cls.artists:
            if artist.artisthash == artisthash:
                artist.colors = color
                break

    @classmethod
    def add_artist(cls, artist: Artist):
        """
        Adds an artist to the store.
        """
        cls.artists.append(artist)

    @classmethod
    def add_artists(cls, artists: list[Artist]):
        """
        Adds multiple artists to the store.
        """
        for artist in artists:
            if artist not in cls.artists:
                cls.artists.append(artist)

    @classmethod
    def get_artist_by_hash(cls, artisthash: str) -> Artist:
        """
        Returns an artist by its hash.
        """
        artists = sorted(cls.artists, key=lambda x: x.artisthash)
        artist = UseBisection(artists, "artisthash", [artisthash])()[0]
        return artist

    @classmethod
    def artist_exists(cls, artisthash: str) -> bool:
        """
        Checks if an artist exists.
        """
        return artisthash in "-".join([a.artisthash for a in cls.artists])

    @classmethod
    def artist_has_tracks(cls, artisthash: str) -> bool:
        """
        Checks if an artist has tracks.
        """
        artists: set[str] = set()

        for track in cls.tracks:
            artists.update(track.artist_hashes)
            album_artists: list[str] = [
                a.artisthash for a in track.albumartist]
            artists.update(album_artists)

        master_hash = "-".join(artists)
        return artisthash in master_hash

    @classmethod
    def remove_artist_by_hash(cls, artisthash: str):
        """
        Removes an artist from the store.
        """
        cls.artists = [a for a in cls.artists if a.artisthash != artisthash]
