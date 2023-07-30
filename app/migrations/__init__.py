"""
Migrations module.

Reads and applies the latest database migrations.

PLEASE NOTE: OLDER MIGRATIONS CAN NEVER BE DELETED.
ONLY MODIFY OLD MIGRATIONS FOR BUG FIXES OR ENHANCEMENTS ONLY
[TRY NOT TO MODIFY BEHAVIOR, UNLESS YOU KNOW WHAT YOU'RE DOING].

PS: Fuck that! Do what you want.
"""


from app.db.sqlite.migrations import MigrationManager
from app.logger import log
from app.migrations import v1_3_0

migrations = [
    [
        # v1.3.0
        v1_3_0.RemovePlaylistArtistHashes,
        v1_3_0.AddSettingsToPlaylistTable,
        v1_3_0.AddLastUpdatedToTrackTable,
        v1_3_0.MovePlaylistsAndFavoritesTo10BitHashes,
        v1_3_0.RemoveAllTracks,
    ]
]


def apply_migrations():
    """
    Applies the latest database migrations.
    """

    version = MigrationManager.get_version()

    # is clean install
    if version == -1:
        MigrationManager.set_version(len(migrations))
        return

    if version != len(migrations):
        # run migrations after the previous migration version
        for migration in migrations[(version - 1) :]:
            for m in migration:
                log.info("Running new migration: %s", m.name)
                m.migrate()

    # bump migration version
    MigrationManager.set_version(len(migrations))
