"""
Pre-init migrations are executed before the database is created.
Useful when you need to move files or folders before the database is created.

`Example use cases: Moving files around, dropping tables, etc.`

PLEASE NOTE: OLDER MIGRATIONS CAN NEVER BE DELETED.
ONLY MODIFY OLD MIGRATIONS FOR BUG FIXES OR ENHANCEMENTS ONLY.
[TRY NOT TO MODIFY BEHAVIOR, UNLESS YOU KNOW WHAT YOU'RE DOING].
"""
from sqlite3 import OperationalError

from app.db.sqlite.migrations import MigrationManager
from app.logger import log

from .drop_artist_and_album_color_tables import DropArtistAndAlbumColorTables
from .move_to_xdg_folder import MoveToXdgFolder

all_preinits = [MoveToXdgFolder, DropArtistAndAlbumColorTables]


def run_preinit_migrations():
    """
    Runs all pre-init migrations.
    """
    try:
        userdb_version = MigrationManager.get_preinit_version()
    except OperationalError:
        userdb_version = 0

    for migration in all_preinits:
        if migration.version > userdb_version:
            log.warn("Running new pre-init migration: %s", migration.name)
            migration.migrate()


def set_preinit_migration_versions():
    """
    Sets the migration versions.
    """
    MigrationManager.set_preinit_version(all_preinits[-1].version)
