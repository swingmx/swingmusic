"""
Another shot at attempting to fix duplicate album and artist color entries.
This release should finally fix the issue. The migration script will now remove
the album and artist color tables and recreate them.
"""

from app.db.sqlite.utils import SQLiteManager
from app.logger import log


class DropArtistAndAlbumColorTables:
    version = 2
    name = "DropArtistAndAlbumColorTables"

    @staticmethod
    def migrate():
        with SQLiteManager() as cur:
            tables = ["artists", "albums"]
            for table in tables:
                cur.execute(f"DROP TABLE IF EXISTS {table}")

            cur.execute("VACUUM")

        log.info("Deleted artist and album color data to fix a few bugs. ✅")
