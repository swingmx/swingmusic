from concurrent.futures import ThreadPoolExecutor
import os
from tqdm import tqdm

from app import settings
from app.db.sqlite.tracks import SQLiteTrackMethods
from app.db.sqlite.settings import SettingsSQLMethods as sdb
from app.db.store import Store

from app.lib.taglib import extract_thumb, get_tags
from app.logger import log
from app.models import Album, Artist, Track
from app.utils import run_fast_scandir

get_all_tracks = SQLiteTrackMethods.get_all_tracks
insert_many_tracks = SQLiteTrackMethods.insert_many_tracks


class Populate:
    """
    Populates the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to extract it.
    """

    def __init__(self) -> None:
        messages = {
            "root_unset": "The root directory is not set. Trying to scan the default directory: %s",
            "default_not_exists": "The directory: %s does not exist. Please open the app in your web browser to set the root directory.",
            "no_tracks": "No tracks found in: %s. Please open the app in your web browser to set the root directory.",
        }

        tracks = get_all_tracks()
        tracks = list(tracks)

        dirs_to_scan = sdb.get_root_dirs()
        initial_dirs_count = len(dirs_to_scan)

        def_dir = "~/Music"

        if len(dirs_to_scan) == 0:
            log.warning(messages["root_unset"], def_dir)
            print("...")

            exists = os.path.exists(settings.MUSIC_DIR)

            if not exists:
                log.warning(messages["default_not_exists"], def_dir)
                return

            dirs_to_scan = [settings.MUSIC_DIR]

        files = []

        for _dir in dirs_to_scan:
            files.extend(run_fast_scandir(_dir, full=True)[1])

        untagged = self.filter_untagged(tracks, files)

        if initial_dirs_count == 0 and len(untagged) == 0:
            log.warning(messages["no_tracks"], def_dir)
            return

        if initial_dirs_count == 0 and len(untagged) > 0:
            log.info(
                "%sFound %s tracks 💪 %s",
                settings.TCOLOR.OKGREEN,
                len(untagged),
                settings.TCOLOR.ENDC,
            )
            log.info(
                "%s%s saved as the default root directory. 😶%s",
                settings.TCOLOR.OKGREEN,
                def_dir,
                settings.TCOLOR.ENDC,
            )
            sdb.add_root_dirs(dirs_to_scan)
            return

        if len(untagged) == 0:
            log.info("All clear, no unread files.")
            return

        self.tag_untagged(untagged)

    @staticmethod
    def filter_untagged(tracks: list[Track], files: list[str]):
        tagged_files = [t.filepath for t in tracks]
        return set(files) - set(tagged_files)

    @staticmethod
    def tag_untagged(untagged: set[str]):
        log.info("Found %s new tracks", len(untagged))
        tagged_tracks: list[dict] = []
        tagged_count = 0

        for file in tqdm(untagged, desc="Reading files"):
            tags = get_tags(file)

            if tags is not None:
                tagged_tracks.append(tags)
                track = Track(**tags)

                Store.add_track(track)
                Store.add_folder(track.folder)

                if not Store.album_exists(track.albumhash):
                    Store.add_album(Store.create_album(track))

                for artist in track.artist:
                    if not Store.artist_exists(artist.artisthash):
                        Store.add_artist(Artist(artist.name))

                for artist in track.albumartist:
                    if not Store.artist_exists(artist.artisthash):
                        Store.add_artist(Artist(artist.name))

                tagged_count += 1
            else:
                log.warning("Could not read file: %s", file)

        if len(tagged_tracks) > 0:
            insert_many_tracks(tagged_tracks)

        log.info("Added %s/%s tracks", tagged_count, len(untagged))


def get_image(album: Album):
    for track in Store.tracks:
        if track.albumhash == album.albumhash:
            extract_thumb(track.filepath, track.image)
            break


class ProcessTrackThumbnails:
    def __init__(self) -> None:
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(
                tqdm(
                    pool.map(get_image, Store.albums),
                    total=len(Store.albums),
                    desc="Extracting track images",
                )
            )

            results = [r for r in results]
