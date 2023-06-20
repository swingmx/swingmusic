"""
Migrations module.

Reads and applies the latest database migrations.

PLEASE NOTE: OLDER MIGRATIONS CAN NEVER BE DELETED.
ONLY MODIFY OLD MIGRATIONS FOR BUG FIXES OR ENHANCEMENTS ONLY
[TRY NOT TO MODIFY BEHAVIOR, UNLESS YOU KNOW WHAT YOU'RE DOING].
"""


from app.db.sqlite.migrations import MigrationManager
from app.logger import log

from .main import main_db_migrations
from .userdata import userdata_db_migrations


def apply_migrations():
    """
    Applies the latest database migrations.
    """

    userdb_version = MigrationManager.get_userdatadb_postinit_version()
    maindb_version = MigrationManager.get_maindb_postinit_version()

    # No migrations to run
    if userdb_version == 0 and maindb_version == 0:
        return

    for migration in main_db_migrations:
        if migration.version > maindb_version:
            log.info("Running new MAIN-DB post-init migration: %s", migration.name)
            migration.migrate()

    for migration in userdata_db_migrations:
        if migration.version > userdb_version:
            log.info("Running new USERDATA-DB post-init migration: %s", migration.name)
            migration.migrate()


def set_postinit_migration_versions():
    """
    Sets the post-init migration versions.
    """
    # TODO: Don't forget to remove the zeros below when you add a valid migration 👇.
    MigrationManager.set_maindb_postinit_version(0)
    MigrationManager.set_userdatadb_postinit_version(0)
