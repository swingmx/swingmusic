import os
import shutil
from app.db.sqlite.utils import SQLiteManager
from app.migrations.base import Migration
from app.settings import Paths


class AddTimestampToFavoritesTable(Migration):
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


class MoveHashesToSha1(Migration):
    """
    Moves the 10 bit item hashes from sha256 to sha1 which is
    faster and more lenient on less powerful devices.

    Thanks to [@tcsenpai](https:github.com/tcsenpai) for the contribution.
    """

    pass

    # INFO: Apparentlly, every single table is affected by this migration.
    # NOTE: Use generators to avoid memory issues.


class DeleteOriginalThumbnails(Migration):
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
