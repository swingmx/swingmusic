"""
License validation cron job.

Revalidates the license with the cloud server periodically
to ensure the device is still authorized and the license is active.
"""

from swingmusic.crons.cron import CronJob


class LicenseValidation(CronJob):
    """
    Revalidates license with cloud server every 3 days (72 hours).

    This ensures:
    - Subscription expirations are detected
    - Revoked devices are locked out
    - License state stays synchronized with server
    """

    name: str = "license_validation"
    hours: int = 24  # 1 day

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Validates license with the cloud server.

        Updates in-memory state and persists to license.json.
        Silently handles errors - validation failures will be caught
        when premium features are accessed via @license_required.
        """
        # Import here to avoid circular imports at module load time
        from swingmusic.lib.license import LicenseManager, LicenseError

        try:
            manager = LicenseManager()
            manager.validate()
        except LicenseError:
            # Validation errors are expected (expired, revoked, etc.)
            # The updated state is already saved - premium features
            # will raise appropriate errors when accessed
            pass
        except Exception:
            # Network errors or unexpected issues - fail silently
            # Grace period will apply based on last_validated timestamp
            pass
