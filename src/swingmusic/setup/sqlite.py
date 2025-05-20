"""
Module to setup Sqlite databases and tables.
Applies migrations.
"""

from sqlalchemy import create_engine
from swingmusic.db.userdata import UserTable
from swingmusic.migrations import apply_migrations
from swingmusic.settings import DbPaths

from swingmusic.db.engine import DbEngine
from swingmusic.db import create_all_tables
# from app.db.libdata import create_all as create_user_tables


def run_migrations():
    """
    Run migrations and updates migration version.
    """
    apply_migrations()


def setup_sqlite():
    """
    Create Sqlite databases and tables.
    """
    DbEngine._engine = create_engine(
        f"sqlite+pysqlite:///{DbPaths.get_app_db_path()}",
        echo=False,
        max_overflow=20,
        pool_size=10,
    )

    create_all_tables()
    # create_user_tables()

    if not list(UserTable.get_all()):
        UserTable.insert_default_user()
