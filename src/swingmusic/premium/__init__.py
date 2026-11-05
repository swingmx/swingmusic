import functools
import logging

PREMIUM_AVAILABLE = False

# Placeholder values for symbols that are None-typed in free builds.
MixesPlugin = None
LicenseManager = None
CloudClient = None
LicenseValidation = None
MixesCron = None
ClassicalSync = None
mixes_api = None
ClassicalStore = None
TranscodeStream = None


# Real exception classes are defined here as stubs. When premium source is
# present, the `from swingmusic.premium.license import ...` below rebinds
# these names at module level to the real classes, so `except LicenseError:`
# in non-premium code keeps working in both builds.
class LicenseError(Exception):
    """Base class for license-related errors."""

    pass


class LicenseNotFoundError(LicenseError):
    pass


class LicenseExpiredError(LicenseError):
    pass


class LicenseRevokedError(LicenseError):
    pass


class LicenseValidationError(LicenseError):
    pass


class CloudError(Exception):
    """Base class for cloud API errors."""

    def __init__(self, message: str = "", status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class CloudAuthError(CloudError):
    pass


class CloudNetworkError(CloudError):
    pass


def license_required(func):
    """Free-tier no-op: decorated call always raises LicenseNotFoundError."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise LicenseNotFoundError("Premium features are not available in this build")

    return wrapper


def classical_available() -> bool:
    """
    Whether classical support can run: the premium code is present, the
    setting is on, and the license is valid.
    """
    if ClassicalStore is None or LicenseManager is None:
        return False

    from swingmusic.config import UserConfig

    if not UserConfig().classicalEnabled:
        return False
    try:
        LicenseManager().check_license()
    except LicenseError:
        return False
    return True


def transcoding_available() -> bool:
    """
    Whether stream transcoding can run: the premium code is present and the license is valid.
    """
    if TranscodeStream is None or LicenseManager is None:
        return False

    try:
        LicenseManager().check_license()
    except LicenseError:
        return False
    return True


# Attempt to load real premium implementations. In the private repo these
# files exist; in the public repo they are stripped before push, so the
# ImportError fallback keeps the module functional.
try:
    from swingmusic.premium.mixes import MixesPlugin  # noqa: F401
    from swingmusic.premium.plugins.lyrics import CloudLyricsPlugin  # noqa: F401
    from swingmusic.premium.license import (  # noqa: F401
        LicenseManager,
        LicenseError,
        LicenseNotFoundError,
        LicenseExpiredError,
        LicenseRevokedError,
        LicenseValidationError,
    )
    from swingmusic.premium.cloud import (  # noqa: F401
        CloudClient,
        CloudError,
        CloudAuthError,
        CloudNetworkError,
    )
    from swingmusic.premium.decorators import license_required  # noqa: F401
    from swingmusic.premium.cron import LicenseValidation  # noqa: F401
    from swingmusic.premium.mixes_cron import Mixes as MixesCron  # noqa: F401
    from swingmusic.premium.api_routes import api as mixes_api  # noqa: F401
    from swingmusic.premium.recipes.because import BecauseYouListened  # noqa: F401
    from swingmusic.premium.classical.classicalstore import ClassicalStore  # noqa: F401
    from swingmusic.premium.classical.sync_cron import ClassicalSync  # noqa: F401
    from swingmusic.premium.transcode.stream import TranscodeStream  # noqa: F401

    PREMIUM_AVAILABLE = True
except ImportError as e:
    logging.getLogger(__name__).warning("Premium features unavailable: %s", e)
