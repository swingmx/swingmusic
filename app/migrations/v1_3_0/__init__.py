import json
import os
import shutil
import time
from collections import OrderedDict
from sqlite3 import OperationalError
from typing import Generator

from app.db.sqlite.utils import SQLiteManager
from app.migrations.base import Migration
from app.settings import Paths
from app.utils.decorators import coroutine
from app.utils.hashing import create_hash

# playlists table
# ---------------
# 0: id
# 1: banner_pos
# 2: has_gif
# 3: image
# 4: last_updated
# 5: name
# 6: trackhashes


class RemoveSmallThumbnailFolder(Migration):
    """
    Removes the small thumbnail folder.

    Because we are added a new folder "original" in the same directory, and the small thumbs folder is used to check if an album's thumbnail is already extracted.

    So we need to remove it, to force the app to extract thumbnails for all albums.
    """

    @staticmethod
    def migrate():
        thumbs_sm_path = Paths.get_sm_thumb_path()
        thumbs_lg_path = Paths.get_lg_thumb_path()

        for path in [thumbs_sm_path, thumbs_lg_path]:
            if os.path.exists(path):
                shutil.rmtree(path)

        for path in [thumbs_sm_path, thumbs_lg_path]:
            os.makedirs(path, exist_ok=True)


class RemovePlaylistArtistHashes(Migration):
    """
    removes the artisthashes column from the playlists table.
    """

    @staticmethod
    def migrate():
        # remove artisthashes column
        sql = "ALTER TABLE playlists DROP COLUMN artisthashes"

        with SQLiteManager(userdata_db=True) as cur:
            try:
                cur.execute(sql)
            except OperationalError:
                pass

            cur.close()


class AddSettingsToPlaylistTable(Migration):
    """
    adds the settings column and removes the banner_pos and has_gif columns
    to the playlists table.
    """

    @staticmethod
    def migrate():
        select_playlists_sql = "SELECT * FROM playlists"

        with SQLiteManager(userdata_db=True) as cur:
            create_playlist_table_sql = """CREATE TABLE IF NOT EXISTS playlists (
                id integer PRIMARY KEY,
                image text,
                last_updated text not null,
                name text not null,
                settings text,
                trackhashes text
            );"""

            insert_playlist_sql = """INSERT INTO playlists(
                image,
                last_updated,
                name,
                settings,
                trackhashes
            ) VALUES(:image, :last_updated, :name, :settings, :trackhashes)
            """

            cur.execute(select_playlists_sql)

            # load all playlists
            playlists = cur.fetchall()

            # drop old playlists table
            cur.execute("DROP TABLE playlists")

            # create new playlists table
            cur.execute(create_playlist_table_sql)

            def transform_playlists(pipeline: Generator, playlists: tuple):
                for playlist in playlists:
                    # create dict that matches the new schema
                    p = {
                        "id": playlist[0],
                        "name": playlist[5],
                        "image": playlist[3],
                        "trackhashes": playlist[6],
                        "last_updated": playlist[4],
                        "settings": json.dumps(
                            {
                                "has_gif": False,
                                "banner_pos": playlist[1],
                                "square_img": False,
                                "pinned": False,
                            }
                        ),
                    }

                    pipeline.send(p)

            @coroutine
            def insert_playlist():
                while True:
                    playlist = yield
                    p = OrderedDict(sorted(playlist.items()))
                    cur.execute(insert_playlist_sql, p)

            # insert playlists using a coroutine
            # (my first coroutine)
            pipeline = insert_playlist()
            transform_playlists(pipeline, playlists)
            pipeline.close()

            cur.close()


class AddLastUpdatedToTrackTable(Migration):
    """
    adds the last modified column to the tracks table.
    """

    @staticmethod
    def migrate():
        # add last_mod column and default to current timestamp
        timestamp = time.time()
        sql = f"ALTER TABLE tracks ADD COLUMN last_mod text not null DEFAULT '{timestamp}'"

        with SQLiteManager() as cur:
            try:
                cur.execute(sql)
            except OperationalError:
                pass

            cur.close()


class MovePlaylistsAndFavoritesTo10BitHashes(Migration):
    """
    moves the playlists and favorites to 10 bit hashes.
    """

    @staticmethod
    def migrate():
        def get_track_data_by_hash(trackhash: str, tracks: list[tuple]) -> tuple:
            for track in tracks:
                # trackhash is the 15th bit hash
                if track[15] == trackhash:
                    # return artist, album, title
                    return track[4], track[1], track[13]

        def get_track_by_albumhash(albumhash: str, tracks: list[tuple]) -> tuple:
            for track in tracks:
                # albumhash is the 3rd bit hash
                if track[3] == albumhash:
                    # return album, albumartist
                    return track[1], track[2]

        _base = "SELECT * FROM"
        fetch_playlists_sql = f"{_base} playlists"
        fetch_tracks_sql = f"{_base} tracks"

        update_playlist_hashes_sql = (
            "UPDATE playlists SET trackhashes = :trackhashes WHERE id = :id"
        )
        fetch_favorites_sql = f"{_base} favorites"
        update_fav_sql = "UPDATE favorites SET hash = :hash WHERE id = :id"
        remove_fav_sql = "DELETE FROM favorites WHERE id = :id"

        db_tracks = []

        # read tracks from db
        with SQLiteManager() as cur:
            cur.execute(fetch_tracks_sql)
            db_tracks.extend(cur.fetchall())
            cur.close()

        # update playlists
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(fetch_playlists_sql)
            playlists = cur.fetchall()

            # for each playlist
            for p in playlists:
                pid = p[0]

                # load trackhashes
                trackhashes: list[str] = json.loads(p[5])

                for index, t in enumerate(trackhashes):
                    (artist, album, title) = get_track_data_by_hash(t, db_tracks)

                    # create new hash
                    new_hash = create_hash(artist, album, title, decode=True, limit=10)
                    trackhashes[index] = new_hash

                # convert to string
                trackhashes = json.dumps(trackhashes)

                # save to db
                cur.execute(
                    update_playlist_hashes_sql, {"trackhashes": trackhashes, "id": pid}
                )

            cur.close()

        # update favorites
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(fetch_favorites_sql)
            favorites = cur.fetchall()

            # for each favorite
            for f in favorites:
                fid = f[0]

                fhash: str = f[1]
                ftype: str = f[2]  # "track" || "album"

                if ftype == "album":
                    (album, albumartist) = get_track_by_albumhash(fhash, db_tracks)

                    # create new hash
                    new_hash = create_hash(album, albumartist, decode=True, limit=10)

                    # save to db
                    cur.execute(update_fav_sql, {"hash": new_hash, "id": fid})
                    continue

                if ftype == "track":
                    (artist, album, title) = get_track_data_by_hash(fhash, db_tracks)

                    # create new hash
                    new_hash = create_hash(artist, album, title, decode=True, limit=10)

                    # save to db
                    cur.execute(update_fav_sql, {"hash": new_hash, "id": fid})
                    continue

                # remove favorites that are not track or album. ie. artists
                cur.execute(remove_fav_sql, {"id": fid})

            cur.close()


class RemoveAllTracks(Migration):
    """
    removes all tracks from the tracks table.
    """

    @staticmethod
    def migrate():
        sql = "DELETE FROM tracks"

        with SQLiteManager() as cur:
            cur.execute(sql)
            cur.close()


class UpdateAppSettingsTable(Migration):
    @staticmethod
    def migrate():
        drop_table_sql = "DROP TABLE settings"
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS settings (
            id integer PRIMARY KEY,
            root_dirs text NOT NULL,
            exclude_dirs text,
            artist_separators text NOT NULL default '/,;',
            extract_feat integer NOT NULL DEFAULT 1,
            remove_prod integer NOT NULL DEFAULT 1,
            clean_album_title integer NOT NULL DEFAULT 1,
            remove_remaster integer NOT NULL DEFAULT 1,
            merge_albums integer NOT NULL DEFAULT 0,
            show_albums_as_singles integer NOT NULL DEFAULT 0
        );
        """

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(drop_table_sql)
            cur.execute(create_table_sql)
