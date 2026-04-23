"""
Module to setup Sqlite databases and tables.
Applies migrations.
"""

from sqlalchemy import create_engine
from swingmusic.settings import Paths
from swingmusic.db.engine import DbEngine
from swingmusic.db import create_all_tables


def setup_sqlite():
    """
    Create Sqlite databases and tables.
    """
    DbEngine._engine = create_engine(
        f"sqlite+pysqlite:///{Paths().app_db_path}",
        echo=False,
        max_overflow=20,
        pool_size=10,
    )

    create_all_tables()
