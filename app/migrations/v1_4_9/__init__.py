import os
import shutil
import sqlite3
from time import time
from app.db.sqlite.utils import SQLiteManager
from app.migrations.base import Migration
from app.settings import Paths

import hashlib
from unidecode import unidecode

from app.db.sqlite.tracks import SQLiteTrackMethods as tdb
from app.db.sqlite.playlists import SQLitePlaylistMethods as pdb
from app.db.sqlite.logger.tracks import SQLiteTrackLogger as ldb
from app.utils.hashing import create_hash


def create_sha256_hash(*args: str, decode=False, limit=10) -> str:
    """
    This function creates a case-insensitive, non-alphanumeric chars ignoring hash from the given arguments.

    Example use case:
        - Creating computable IDs for duplicate artists. eg. Juice WRLD and Juice Wrld should have the same ID.

    :param args: The arguments to hash.
    :param decode: Whether to decode the arguments before hashing.
    :param limit: The number of characters to return.

    :return: The hash.
    """

    def remove_non_alnum(token: str) -> str:
        token = token.lower().strip().replace(" ", "")
        t = "".join(t for t in token if t.isalnum())

        if t == "":
            return token

        return t

    str_ = "".join(remove_non_alnum(t) for t in args)

    if decode:
        str_ = unidecode(str_)

    str_ = str_.encode("utf-8")
    str_ = hashlib.sha256(str_).hexdigest()
    return str_[-limit:]


def create_sha1_hash(*args: str, decode=False, limit=10) -> str:
    """
    This function creates a case-insensitive, non-alphanumeric chars ignoring hash from the given arguments.

    Example use case:
        - Creating computable IDs for duplicate artists. eg. Juice WRLD and Juice Wrld should have the same ID.

    :param args: The arguments to hash.
    :param decode: Whether to decode the arguments before hashing.
    :param limit: The number of characters to return.

    :return: The hash.
    """

    def remove_non_alnum(token: str) -> str:
        token = token.lower().strip().replace(" ", "")
        t = "".join(t for t in token if t.isalnum())

        if t == "":
            return token

        return t

    str_ = "".join(remove_non_alnum(t) for t in args)

    if decode:
        str_ = unidecode(str_)

    str_ = str_.encode("utf-8")
    str_ = hashlib.sha1(str_).hexdigest()

    return (
        str_[: limit // 2] + str_[-limit // 2 :]
        if limit % 2 == 0
        else str_[: limit // 2] + str_[-limit // 2 - 1 :]
    )


class _1AddTimestampToFavoritesTable(Migration):
    """
    Adds a timestamp column to the favorites table.
    """

    @staticmethod
    def migrate():
        # INFO: add timestamp column with automatic current timestamp
        sql = f"ALTER TABLE favorites ADD COLUMN timestamp INTEGER NOT NULL DEFAULT 0"

        # INFO: execute the sql
        with SQLiteManager(userdata_db=True) as cur:
            table_exists = cur.execute(
                "select count(*) from pragma_table_info('favorites') where name = 'timestamp'"
            )

            table_exists = table_exists.fetchone()

            if table_exists[0] == 1:
                return

            # INFO: Add the timestamp column to the favorites table
            timestamp = int(time())
            cur.execute(sql)
            cur.execute(f"UPDATE favorites SET timestamp = {timestamp}")


class _2DeleteOriginalThumbnails(Migration):
    """
    Original thumbnails are too large and are not needed.
    """

    # TODO: Implement this migration

    @staticmethod
    def migrate():
        imgpath = Paths.get_thumbs_path()
        og_imgpath = os.path.join(imgpath, "original")

        if os.path.exists(og_imgpath):
            shutil.rmtree(og_imgpath)


class _3MoveScrobbleToUserId1(Migration):
    """
    Updates all track logs from user id = 0 to user id = 1
    """

    @staticmethod
    def migrate():
        sql = """
        UPDATE track_logger SET userid = 1 WHERE userid = 0;
        ALTER TABLE track_logger RENAME TO _track_logger;
        CREATE TABLE IF NOT EXISTS track_logger (
            id integer PRIMARY KEY,
            trackhash text NOT NULL,
            duration integer NOT NULL,
            timestamp integer NOT NULL,
            source text,
            userid integer NOT NULL DEFAULT 1,
            constraint fk_users foreign key (userid) references users(id) on delete cascade
        );

        INSERT INTO track_logger SELECT * FROM _track_logger;
        DROP TABLE _track_logger;
        """
        # INFO: Move the scrobble table to the user id 1
        with SQLiteManager(userdata_db=True) as cur:
            cur.executescript(sql)
            cur.close()


class _4AddUserIdToFavoritesTable(Migration):
    """
    Adds a userid column to the favorites table.
    """

    @staticmethod
    def migrate():
        # check if userid column exists
        exists_sql = (
            "select count(*) from pragma_table_info('favorites') where name = 'userid'"
        )
        sql = """
        ALTER TABLE favorites ADD userid INTEGER NOT NULL DEFAULT 1;
        ALTER TABLE favorites RENAME TO _favorites;

        CREATE TABLE IF NOT EXISTS favorites (
            id integer PRIMARY KEY,
            hash text not null,
            type text not null,
            timestamp integer not null default 0,
            userid integer not null,
            constraint fk_users foreign key (userid) references users(id) on delete cascade
        );

        INSERT INTO favorites SELECT * FROM _favorites;
        DROP TABLE _favorites;
        """

        with SQLiteManager(userdata_db=True) as cur:
            data = cur.execute(exists_sql)
            data = data.fetchone()

            if data[0] == 1:
                return  # INFO: column already exists

            cur.executescript(sql)


class _5AddUserIdToPlaylistsTable(Migration):
    """
    Adds a userid column to the playlists table.
    """

    @staticmethod
    def migrate():
        # check if userid column exists
        exists_sql = (
            "select count(*) from pragma_table_info('playlists') where name = 'userid'"
        )

        # Add the userid column to the playlists table
        # Rename the old table to _playlists
        # Create a new playlists table with the userid column
        # Then, copy the data from the old table to the new table
        # Finally, drop the old table
        sql = """
        ALTER TABLE playlists ADD userid INTEGER NOT NULL DEFAULT 1;
        ALTER TABLE playlists RENAME TO _playlists;
        CREATE TABLE IF NOT EXISTS playlists (
            id integer PRIMARY KEY,
            image text,
            last_updated text not null,
            name text not null,
            settings text,
            trackhashes text,
            userid integer not null,
            constraint fk_users foreign key (userid) references users(id) on delete cascade
        );

        INSERT INTO playlists SELECT * FROM _playlists;
        DROP TABLE _playlists;
        """

        with SQLiteManager(userdata_db=True) as cur:
            # INFO: Check if the column already exists
            data = cur.execute(exists_sql)
            data = data.fetchone()

            # INFO: If the column already exists, return
            if data[0] == 1:
                return  # INFO: column already exists

            # INFO: Execute the sql
            cur.executescript(sql)


class _6MoveHashesToSha1(Migration):
    """
    Moves the 10 bit item hashes from sha256 to sha1 which is
    faster and more lenient on less powerful devices.

    Thanks to [@tcsenpai](https:github.com/tcsenpai) for the contribution.
    """

    # enabled: bool = False

    # pass

    # INFO: Apparentlly, every single table is affected by this migration.
    # NOTE: Use generators to avoid memory issues.

    @classmethod
    def port_track(cls, trackhash: str):
        # get the track with the track hash
        track = tdb.get_track_by_trackhash(trackhash)

        if track is None:
            return

        title = track.og_title
        if track.trackhash != trackhash:
            # raise ValueError("Track hash mismatch")
            print("Track hash mismatch")
            title = track.title
        else:
            print("Porting track: ", track.title)

        # return the new hash
        finalhash = create_sha1_hash(
            ", ".join(a.name for a in track.artists),
            track.og_album,
            title,
        )

        if finalhash != create_hash(
            ", ".join(a.name for a in track.artists), track.og_album, title
        ):
            raise ValueError("Hash mismatch")

    @classmethod
    def port_album(cls, albumhash: str):
        # get the first track with the album hash
        track = tdb.get_track_by_albumhash(albumhash)

        if track is None:
            return

        # return the new hash
        return create_sha1_hash(
            track.og_album,
            ", ".join(a.name for a in track.albumartists),
        )

    @classmethod
    def port_artist(cls, artisthash: str):
        # find all tracks with the artist hash
        tracks = [t for t in cls.tracks if artisthash in t.artist_hashes]

        if len(tracks) == 0:
            return

        # find the artist name
        artist = [
            a.name
            for a in tracks[0].artists
            if create_sha256_hash(a.name, decode=True) == artisthash
        ][0]

        # return the new hash
        return create_sha1_hash(artist, decode=True)

    @classmethod
    def migrate_favorites(cls):
        with SQLiteManager(userdata_db=True) as cur:
            # read all favorites
            data = cur.execute("SELECT * FROM favorites")
            data = data.fetchall()

            for track in cls.tracks:
                track.artist_hashes = "-".join(
                    [create_sha256_hash(a.name, decode=True) for a in track.artists]
                )

            for entry in data:
                # hash is the 2nd column in the table
                hash = entry[1]

                # entry type is the 3rd column in the table
                if entry[2] == "track":
                    newhash = cls.port_track(hash)

                    if newhash:
                        cur.execute(
                            f"UPDATE favorites SET hash = '{newhash}' WHERE hash = '{hash}' AND type = 'track'"
                        )

                elif entry[2] == "album":
                    newhash = cls.port_album(hash)

                    if newhash:
                        cur.execute(
                            f"UPDATE favorites SET hash = '{newhash}' WHERE hash = '{hash}' AND type = 'album'"
                        )

                elif entry[2] == "artist":
                    newhash = cls.port_artist(hash)

                    if newhash:
                        cur.execute(
                            f"UPDATE favorites SET hash = '{newhash}' WHERE hash = '{hash}' AND type = 'artist'"
                        )

    @classmethod
    def migrate_playlists(cls):
        playlists = pdb.get_all_playlists()

        for playlist in playlists:
            # remove previous hashes
            to_remove = [
                {"trackhash": trackhash, "index": index}
                for index, trackhash in enumerate(playlist.trackhashes)
            ]
            pdb.remove_tracks_from_playlist(playlist.id, to_remove)

            # add new hashes
            newhashes = [
                cls.port_track(trackhash) for trackhash in playlist.trackhashes
            ]
            newhashes = [h for h in newhashes if h is not None]
            pdb.add_tracks_to_playlist(playlist.id, newhashes)

            print("Ported playlist: ", playlist.name)
            print("Total tracks: ", len(newhashes))

    @classmethod
    def migrate_scrobble(cls):
        # read all logs
        logs = ldb.get_all()

        with SQLiteManager(userdata_db=True) as cur:
            # for each log, port the hash
            for log in logs:
                newhash = cls.port_track(log[1])

                if newhash:
                    cur.execute(
                        f"UPDATE track_logger SET trackhash = '{newhash}' WHERE trackhash = '{log[1]}'"
                    )

    @classmethod
    def migrate(cls):
        cls.tracks = list(tdb.get_all_tracks())
        cls.migrate_favorites()
        # cls.migrate_playlists()
        # cls.migrate_scrobble()
