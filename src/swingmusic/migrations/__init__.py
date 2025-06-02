"""
Migrations module.

Reads and applies the latest database migrations.
"""

import inspect
from types import ModuleType

# from app.db.sqlite.migrations import MigrationManager
from swingmusic.db.metadata import MigrationTable
from swingmusic.migrations.base import Migration


def get_all_migrations(module: ModuleType) -> list[Migration]:
    """
    Extracts all migration classes from a module.
    """
    predicate = (
        lambda obj: inspect.isclass(obj)
        and issubclass(obj, Migration)
        and obj.enabled
        and obj.__module__ == module.__name__
    )

    # INFO: I couldn't find how to sort the classes in order of appearance
    # so I just renamed them to be sortable by name
    return [obj for name, obj in inspect.getmembers(module, predicate)]


def apply_migrations():
    """
    Applies the latest database migrations.

    The length of all the migrations is stored in the database
    and used to check for new migrations. When the length of the
    migrations list is larger than the number stored in the db,
    migrations past that index are applied and the new length
    is stored as the new migration index.
    """
    modules = []
    migrations = [get_all_migrations(m) for m in modules]

    # index = MigrationManager.get_index()
    index = MigrationTable.get_version()
    all_migrations = [migration for sublist in migrations for migration in sublist]

    to_apply: list[Migration] = []

    # if index is from old release,
    # get migrations from the "migrations" list
    
    # if index < 3:
    #     _migrations = migrations[index:]
    #     to_apply = [migration for sublist in _migrations for migration in sublist]
    # else:
    #     to_apply = all_migrations[index:]

    # for migration in to_apply:
    #     # try:
    #     migration.migrate()
    #     log.info("Applied migration: %s", migration.__name__)
    # except Exception as e:
    #     log.error("Failed to run migration: %s", migration.__name__)
    #     log.error(e)

    # sys.exit(0)
    # MigrationManager.set_index(len(all_migrations))
    MigrationTable.set_version(len(all_migrations))
