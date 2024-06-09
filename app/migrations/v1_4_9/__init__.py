import os
import shutil
from app.db.sqlite.utils import SQLiteManager
from app.migrations.base import Migration
from app.settings import Paths


class _1AddTimestampToFavoritesTable(Migration):
    """
    Adds a timestamp column to the favorites table.
    """

    @staticmethod
    def migrate():
        # INFO: add timestamp column with automatic current timestamp
        sql = f"ALTER TABLE favorites ADD COLUMN IF NOT EXISTS timestamp INTEGER NOT NULL DEFAULT 0"

        # INFO: execute the sql
        with SQLiteManager(userdata_db=True) as cur:
            try:
                # INFO: Add the timestamp column to the favorites table
                cur.execute(sql)

                # INFO: Set all the timestamps to the current time
                cur.execute("UPDATE favorites SET timestamp = strftime('%s', 'now')")
            except Exception as e:
                # INFO: timestamp column already exists
                pass
            finally:
                cur.close()


class _4MoveHashesToSha1(Migration):
    """
    Moves the 10 bit item hashes from sha256 to sha1 which is
    faster and more lenient on less powerful devices.

    Thanks to [@tcsenpai](https:github.com/tcsenpai) for the contribution.
    """

    enabled: bool = False

    pass

    # INFO: Apparentlly, every single table is affected by this migration.
    # NOTE: Use generators to avoid memory issues.


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
        # INFO: Move the scrobble table to the user id 1
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute("UPDATE track_logger SET userid = 1 WHERE userid = 0")
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
                return # INFO: column already exists

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
