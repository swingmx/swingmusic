from app.db.sqlite.utils import SQLiteManager
from app.utils import win_replace_slash


class SettingsSQLMethods:
    """
    Methods for interacting with the settings table.
    """

    @staticmethod
    def get_root_dirs() -> list[str]:
        """
        Gets custom root directories from the database.
        """

        sql = "SELECT root_dirs FROM settings"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            dirs = cur.fetchall()

            dirs = [dir[0] for dir in dirs]
            return [win_replace_slash(d) for d in dirs]

    @staticmethod
    def add_root_dirs(dirs: list[str]):
        """
        Add custom root directories to the database.
        """

        sql = "INSERT INTO settings (root_dirs) VALUES (?)"
        existing_dirs = SettingsSQLMethods.get_root_dirs()

        dirs = [dir for dir in dirs if dir not in existing_dirs]

        if len(dirs) == 0:
            return

        with SQLiteManager(userdata_db=True) as cur:
            for _dir in dirs:
                cur.execute(sql, (_dir,))

    @staticmethod
    def remove_root_dirs(dirs: list[str]):
        """
        Remove custom root directories from the database.
        """

        sql = "DELETE FROM settings WHERE root_dirs = ?"

        with SQLiteManager(userdata_db=True) as cur:
            for _dir in dirs:
                cur.execute(sql, (_dir,))

    @staticmethod
    def add_excluded_dirs(dirs: list[str]):
        """
        Add custom exclude directories to the database.
        """

        sql = "INSERT INTO settings (exclude_dirs) VALUES (?)"

        with SQLiteManager(userdata_db=True) as cur:
            cur.executemany(sql, dirs)

    @staticmethod
    def remove_excluded_dirs(dirs: list[str]):
        """
        Remove custom exclude directories from the database.
        """

        sql = "DELETE FROM settings WHERE exclude_dirs = ?"

        with SQLiteManager(userdata_db=True) as cur:
            cur.executemany(sql, dirs)

    @staticmethod
    def get_excluded_dirs() -> list[str]:
        """
        Gets custom exclude directories from the database.
        """

        sql = "SELECT exclude_dirs FROM settings"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            dirs = cur.fetchall()
            return [dir[0] for dir in dirs]
