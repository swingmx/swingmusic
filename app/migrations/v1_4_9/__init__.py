from app.db.sqlite.utils import SQLiteManager
from app.migrations.base import Migration


class AddTimestampToFavoritesTable(Migration):
    """
    Adds a timestamp column to the favorites table.
    """

    @staticmethod
    def migrate():
        # INFO: add timestamp column with automatic current timestamp
        sql = f"ALTER TABLE favorites ADD COLUMN timestamp INTEGER NOT NULL DEFAULT 0"

        # INFO: execute the sql
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)

            # INFO: Update the timestamp column with the current timestamp
            cur.execute("UPDATE favorites SET timestamp = strftime('%s', 'now')")
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