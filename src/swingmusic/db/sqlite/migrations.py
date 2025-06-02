"""
Reads and saves the latest database migrations version.
"""

from swingmusic.db.sqlite.utils import SQLiteManager


class MigrationManager:
    @staticmethod
    def get_index() -> int:
        """
        Returns the latest databases migrations index.
        """
        sql = "SELECT * FROM dbmigrations"
        with SQLiteManager() as cur:
            cur.execute(sql)
            ver = int(cur.fetchone()[1])
            cur.close()

            return ver

    # 👇 Setters 👇
    @staticmethod
    def set_index(version: int):
        """
        Updates the databases migrations index.
        """
        sql = "UPDATE dbmigrations SET version = ? WHERE id = 1"
        with SQLiteManager() as cur:
            cur.execute(sql, (version,))
            cur.close()
