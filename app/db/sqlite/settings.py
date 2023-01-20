import json
from app.db.sqlite.utils import SQLiteManager


class SettingsSQLMethods:
    """
    Methods for interacting with the settings table.
    """

    @staticmethod
    def update_root_dirs(dirs: list[str]):
        """
        Updates custom root directories in the database.
        """

        sql = "UPDATE settings SET root_dirs = ?"
        dirs_str = json.dumps(dirs)

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (dirs_str,))

    @staticmethod
    def get_root_dirs() -> list[str]:
        """
        Gets custom root directories from the database.
        """

        sql = "SELECT value FROM settings"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)

            data = cur.fetchone()

            if data is not None:
                return json.loads(data[0])

            return []

    @staticmethod
    def update_exclude_dirs(dirs: list[str]):
        """
        Updates excluded directories in the database.
        """

        sql = "UPDATE settings SET exclude_dirs = ?"
        dirs_str = json.dumps(dirs)

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (dirs_str,))
