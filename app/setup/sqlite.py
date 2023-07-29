"""
Module to setup Sqlite databases and tables.
Applies migrations.
"""

from app.db.sqlite import create_connection, create_tables, queries
from app.migrations import apply_migrations
from app.settings import Db


def run_migrations():
    """
    Run migrations and updates migration version.
    """
    apply_migrations()


def setup_sqlite():
    """
    Create Sqlite databases and tables.
    """
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)

    app_db_conn = create_connection(Db.get_app_db_path())
    user_db_conn = create_connection(Db.get_userdata_db_path())

    create_tables(app_db_conn, queries.CREATE_APPDB_TABLES)
    create_tables(user_db_conn, queries.CREATE_USERDATA_TABLES)
    create_tables(app_db_conn, queries.CREATE_MIGRATIONS_TABLE)

    app_db_conn.close()
    user_db_conn.close()
