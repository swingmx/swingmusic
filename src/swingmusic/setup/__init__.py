"""
Prepares the server for use.
"""

from dataclasses import asdict
from time import time
import uuid

from swingmusic.config import UserConfig
from swingmusic.lib.crypto import Cryptography
from swingmusic.db.userdata import UserTable
from swingmusic.lib.mapstuff import (
    map_album_colors,
    map_artist_colors,
    map_favorites,
    map_scrobble_data,
)
from swingmusic.setup.sqlite import setup_sqlite
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.folder import FolderStore
from swingmusic.store.general import GeneralStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.generators import get_random_str


def _validate_license():
    """
    Validates the license with the cloud server on startup.

    If a license key exists, attempts to validate with the server.
    Failures are handled gracefully - the LicenseManager state will
    reflect the validation result, and premium features will be
    gated accordingly. In free builds (premium modules absent),
    this is a no-op.
    """
    from swingmusic.premium import LicenseManager, LicenseError

    if LicenseManager is None:
        # Premium not available in this build; nothing to validate.
        return

    try:
        manager = LicenseManager()
        manager.validate()
    except LicenseError:
        # Validation errors (expired, revoked, not registered)
        # State is already updated - premium features will be disabled
        pass
    except Exception:
        # Network errors or unexpected issues
        # Grace period will apply based on last_validated timestamp
        pass


def is_uuid4(value: str) -> bool:
    """
    Check if a string is a valid UUID4 used in pre-v3
    """
    try:
        uuid.UUID(value)
    except (ValueError, TypeError):
        return False

    return True


def run_setup():
    """
    Creates the config directory, runs migrations, and loads settings.
    """

    # setup config file
    config = UserConfig()
    config.setup_config_file()

    if config.serverId and is_uuid4(config.serverId):
        # Save legacy serverId to legacy_serverId
        config.legacy_serverId = config.serverId
        config.serverId = ""
        config.write_to_file(asdict(config))

    if not config.serverId or not Cryptography.private_key_exists():
        # Generate new ed25519 keypair
        crypto = Cryptography()

        # Set serverId to the public key
        config.serverId = crypto.public_key
        config.write_to_file(asdict(config))

    setup_sqlite()
    # Validate license on startup
    _validate_license()


def load_into_mem():
    """
    Load all tracks, albums, and artists into memory.
    """
    # INFO: Load all tracks, albums, and artists data into memory
    key = str(time())
    GeneralStore.load_onboarding_data(list(UserTable.get_all()))
    TrackStore.load_all_tracks(get_random_str())
    AlbumStore.load_albums(key)
    ArtistStore.load_artists(key)
    FolderStore.load_filepaths()

    map_scrobble_data()
    map_favorites()
    map_artist_colors()
    map_album_colors()
