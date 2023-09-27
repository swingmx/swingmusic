from pprint import pprint
from typing import Any

from app.db.sqlite.utils import SQLiteManager
from app.settings import SessionVars
from app.utils.wintools import win_replace_slash


class SettingsSQLMethods:
    """
    Methods for interacting with the settings table.
    """

    @staticmethod
    def get_all_settings():
        """
        Gets all settings from the database.
        """

        sql = "SELECT * FROM settings WHERE id = 1"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            settings = cur.fetchone()
            cur.close()

            # if root_dirs not set
            if settings is None:
                return []

            # omit id, root_dirs, and exclude_dirs
            return settings[3:]

    @staticmethod
    def get_root_dirs() -> list[str]:
        """
        Gets custom root directories from the database.
        """

        sql = "SELECT root_dirs FROM settings"

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            dirs = cur.fetchall()
            cur.close()

            dirs = [_dir[0] for _dir in dirs]
            return [win_replace_slash(d) for d in dirs]

    @staticmethod
    def add_root_dirs(dirs: list[str]):
        """
        Add custom root directories to the database.
        """

        sql = "INSERT INTO settings (root_dirs) VALUES (?)"
        existing_dirs = SettingsSQLMethods.get_root_dirs()

        dirs = [_dir for _dir in dirs if _dir not in existing_dirs]

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

    # Not currently used anywhere, to be used later
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
            return [_dir[0] for _dir in dirs]

    @staticmethod
    def get_settings() -> dict[str, Any]:
        pass

    @staticmethod
    def set_setting(key: str, value: Any):
        sql = f"UPDATE settings SET {key} = :value WHERE id = 1"

        if type(value) == bool:
            value = str(int(value))

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, {"value": value})


def load_settings():
    s = SettingsSQLMethods.get_all_settings()

    try:
        db_separators: str = s[0]
        db_separators = db_separators.replace(" ", "")
        separators = db_separators.split(",")
        separators = set(separators)
    except IndexError:
        separators = {";", "/"}

    SessionVars.ARTIST_SEPARATORS = separators

    # boolean settings
    SessionVars.EXTRACT_FEAT = bool(s[1])
    SessionVars.REMOVE_PROD = bool(s[2])
    SessionVars.CLEAN_ALBUM_TITLE = bool(s[3])
    SessionVars.REMOVE_REMASTER_FROM_TRACK = bool(s[4])
    SessionVars.MERGE_ALBUM_VERSIONS = bool(s[5])
    SessionVars.SHOW_ALBUMS_AS_SINGLES = bool(s[6])
