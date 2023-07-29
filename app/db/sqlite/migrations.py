"""
Reads and saves the latest database migrations version.
"""

from app.db.sqlite.utils import SQLiteManager


class MigrationManager:
    @staticmethod
    def get_version() -> int:
        """
        Returns the latest userdata database version.
        """
        sql = "SELECT * FROM dbmigrations"
        with SQLiteManager() as cur:
            cur.execute(sql)
            ver = int(cur.fetchone()[1])
            cur.close()

            return ver

    # 👇 Setters 👇
    @staticmethod
    def set_version(version: int):
        """
        Sets the userdata pre-init database version.
        """
        sql = "UPDATE dbmigrations SET version = ? WHERE id = 1"
        with SQLiteManager() as cur:
            cur.execute(sql, (version,))
            cur.close()
