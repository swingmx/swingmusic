"""
Reads and saves the latest database migrations version.
"""

from app.db.sqlite.utils import SQLiteManager


class MigrationManager:
    all_get_sql = "SELECT * FROM migrations"

    _base = "UPDATE migrations SET"
    _end = "= ? WHERE id = 1"

    pre_init_set_sql = f"{_base} pre_init_version {_end}"
    post_init_set_sql = f"{_base} post_init_version {_end}"

    @classmethod
    def get_preinit_version(cls) -> int:
        """
        Returns the latest userdata pre-init database version.
        """
        with SQLiteManager() as cur:
            cur.execute(cls.all_get_sql)
            return int(cur.fetchone()[1])

    @classmethod
    def get_maindb_postinit_version(cls) -> int:
        """
        Returns the latest maindb post-init database version.
        """
        with SQLiteManager() as cur:
            cur.execute(cls.all_get_sql)
            return int(cur.fetchone()[2])

    @classmethod
    def get_userdatadb_postinit_version(cls) -> int:
        """
        Returns the latest userdata post-init database version.
        """
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(cls.all_get_sql)
            return cur.fetchone()[2]

    # 👇 Setters 👇
    @classmethod
    def set_preinit_version(cls, version: int):
        """
        Sets the userdata pre-init database version.
        """
        with SQLiteManager() as cur:
            cur.execute(cls.pre_init_set_sql, (version,))

    @classmethod
    def set_maindb_postinit_version(cls, version: int):
        """
        Sets the maindb post-init database version.
        """
        with SQLiteManager() as cur:
            cur.execute(cls.post_init_set_sql, (version,))

    @classmethod
    def set_userdatadb_postinit_version(cls, version: int):
        """
        Sets the userdata post-init database version.
        """
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(cls.post_init_set_sql, (version,))
