"""
Migrations module.

Reads and applies the latest database migrations.
"""

from app.db.sqlite.migrations import MigrationManager
from app.logger import log
from app.migrations import v1_3_0, v1_4_9
from app.migrations.base import Migration

migrations: list[list[Migration]] = [
    [
        # v1.3.0
        v1_3_0.RemoveSmallThumbnailFolder,
        v1_3_0.RemovePlaylistArtistHashes,
        v1_3_0.AddSettingsToPlaylistTable,
        v1_3_0.AddLastUpdatedToTrackTable,
        v1_3_0.MovePlaylistsAndFavoritesTo10BitHashes,
        v1_3_0.RemoveAllTracks,
        v1_3_0.UpdateAppSettingsTable,
    ],
    [v1_4_9.AddTimestampToFavoritesTable, v1_4_9.DeleteOriginalThumbnails],
]


def apply_migrations():
    """
    Applies the latest database migrations.

    The length of all the migrations is stored in the database
    and used to check for new migrations. When the length of the
    migrations list is larger than the number stored in the db,
    migrations past that index are applied and the new length
    is stored as the new migration index.
    """

    index = MigrationManager.get_index()
    all_migrations = [migration for sublist in migrations for migration in sublist]

    to_apply: list[Migration] = []

    # if index is from old release,
    # get migrations from the "migrations" list
    if index < 3:
        _migrations = migrations[index:]
        to_apply = [migration for sublist in _migrations for migration in sublist]
    else:
        to_apply = all_migrations[index:]

    for migration in to_apply:
        try:
            migration.migrate()
            log.info("Applied migration: %s", migration.__name__)
        except:
            log.error("Failed to run migration: %s", migration.__name__)

    MigrationManager.set_index(len(all_migrations))
