"""
Module to setup Sqlite databases and tables.
Applies migrations.
"""

from app.db.sqlite import create_connection, create_tables, queries
from app.migrations import apply_migrations, set_postinit_migration_versions
from app.migrations.__preinit import run_preinit_migrations, set_preinit_migration_versions

from app.settings import APP_DB_PATH, USERDATA_DB_PATH


def setup_sqlite():
    """
    Create Sqlite databases and tables.
    """
    # if os.path.exists(DB_PATH):
    #     os.remove(DB_PATH)

    run_preinit_migrations()

    app_db_conn = create_connection(APP_DB_PATH)
    playlist_db_conn = create_connection(USERDATA_DB_PATH)

    create_tables(app_db_conn, queries.CREATE_APPDB_TABLES)
    create_tables(playlist_db_conn, queries.CREATE_USERDATA_TABLES)

    create_tables(app_db_conn, queries.CREATE_MIGRATIONS_TABLE)
    create_tables(playlist_db_conn, queries.CREATE_MIGRATIONS_TABLE)

    app_db_conn.close()
    playlist_db_conn.close()


def run_migrations():
    """
    Run migrations and updates migration version.
    """
    apply_migrations()
    set_preinit_migration_versions()
    set_postinit_migration_versions()
