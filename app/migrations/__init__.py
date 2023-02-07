"""
Migrations module.

Reads and applies the latest database migrations.
"""
from .main import main_db_migrations
from .userdata import userdata_db_migrations


def apply_migrations():
    userdb_version = 0
    maindb_version = 0

    for migration in main_db_migrations:
        if migration.version > maindb_version:
            migration.migrate()

    for migration in userdata_db_migrations:
        if migration.version > userdb_version:
            migration.migrate()
