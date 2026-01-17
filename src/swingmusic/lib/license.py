"""
License management with in-memory state and file-based caching.

The LicenseManager maintains license state in memory as the source of truth.
The license.json file is only used as a cache for persistence across restarts.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from swingmusic.config import UserConfig
from swingmusic.lib.cloud import CloudClient, CloudAuthError, CloudNetworkError
from swingmusic.settings import Paths, Singleton
from swingmusic.utils.hardware_id import get_device_id


# =============================================================================
# Exceptions
# =============================================================================


class LicenseError(Exception):
    """Base exception for license issues."""

    pass


class LicenseNotFoundError(LicenseError):
    """No license key configured or license not activated."""

    pass


class LicenseExpiredError(LicenseError):
    """License has expired."""

    pass


class LicenseRevokedError(LicenseError):
    """Device was revoked from license."""

    pass


class LicenseValidationError(LicenseError):
    """Failed to validate with server and grace period exceeded."""

    pass


# =============================================================================
# LicenseManager
# =============================================================================


class LicenseManager(metaclass=Singleton):
    """
    Manages license state in memory with file-based caching.

    Key design decisions:
    - _state: in-memory source of truth (never read from file after init)
    - license.json: cache file, written after every validation
    - check_license(): reads from _state only
    - validate(): calls server → updates _state → writes file
    - register(): calls server → updates _state → writes file

    This prevents users from just editing license.json to bypass checks,
    since the file is only loaded once at startup and immediately validated.
    """

    GRACE_PERIOD_DAYS = 3

    def __init__(self):
        self._license_file: Path = Paths().config_dir / "license.json"
        self._state: dict[str, Any] = {}
        self._license_key: str = ""

        self._load_from_cache()
        self._license_key = UserConfig().licenseKey or ""

    @property
    def license_key(self) -> str:
        """The license key from UserConfig."""
        return self._license_key

    @property
    def is_registered(self) -> bool:
        """Whether a license key is configured."""
        return bool(self._license_key)

    @property
    def state(self) -> dict[str, Any]:
        """Read-only access to current license state."""
        return self._state.copy()

    def _load_from_cache(self) -> None:
        """Load license.json into memory (startup only)."""
        if self._license_file.exists():
            try:
                self._state = json.loads(self._license_file.read_text())
            except (json.JSONDecodeError, IOError):
                self._state = {}
        else:
            self._state = {}

    def _save_to_cache(self) -> None:
        """Persist current _state to license.json."""
        try:
            self._license_file.write_text(json.dumps(self._state, indent=2))
        except IOError:
            pass  # Fail silently - memory state is still valid

    def _delete_cache(self) -> None:
        """Delete the license.json cache file."""
        try:
            if self._license_file.exists():
                self._license_file.unlink()
        except IOError:
            pass

    def _parse_datetime(self, dt_str: str | None) -> datetime | None:
        """Parse ISO datetime string to datetime object."""
        if not dt_str:
            return None
        try:
            # Handle both Z suffix and +00:00 formats
            if dt_str.endswith("Z"):
                dt_str = dt_str[:-1] + "+00:00"
            return datetime.fromisoformat(dt_str)
        except ValueError:
            return None

    def check_license(self) -> None:
        """
        Validates license from in-memory state.

        This method reads ONLY from _state (memory), never from file.
        Called by @license_required decorator.

        Raises:
            LicenseNotFoundError: No license key or not activated
            LicenseExpiredError: License has expired
            LicenseRevokedError: Device was revoked
            LicenseValidationError: Grace period exceeded
        """
        # 1. No license key configured
        if not self._license_key:
            raise LicenseNotFoundError("No license key configured")

        # 2. No state loaded (not activated)
        if not self._state or "user" not in self._state:
            raise LicenseNotFoundError("License not activated")

        user = self._state.get("user", {})

        # 3. Check status
        status = user.get("status", "")
        if status == "revoked":
            raise LicenseRevokedError("License has been revoked")
        if status == "expired":
            raise LicenseExpiredError("License has expired")
        if status != "active":
            raise LicenseError(f"Invalid license status: {status}")

        # 4. Check expiry (for subscriptions/time_limited)
        expires_at = self._parse_datetime(user.get("expires_at"))
        if expires_at:
            now = datetime.now(timezone.utc)
            if expires_at < now:
                raise LicenseExpiredError("Subscription has expired")

        # 5. Check device is in list
        my_device_id = get_device_id()
        devices = self._state.get("devices", {}).get("list", [])
        device_ids = [d.get("device_id") for d in devices]
        if my_device_id not in device_ids:
            raise LicenseRevokedError("This device is no longer authorized")

        # 6. Check grace period (3 days since last validation)
        meta = self._state.get("_meta", {})
        last_validated = self._parse_datetime(meta.get("last_validated"))
        if last_validated:
            now = datetime.now(timezone.utc)
            days_since = (now - last_validated).days
            if days_since > self.GRACE_PERIOD_DAYS:
                raise LicenseValidationError(
                    f"License validation expired ({days_since} days since last check). "
                    "Please connect to the internet to re-validate."
                )

    def validate(self) -> bool:
        """
        Validate license with cloud server using GET /auth/status.

        Updates _state with server response and writes to cache file.
        Called on startup and by the periodic cron job.

        Returns:
            True: License valid, state updated
            False: Server unreachable (grace period applies)

        Raises:
            LicenseNotFoundError: User not registered (401)
            LicenseExpiredError: License expired (403 with expired)
            LicenseRevokedError: Device revoked (403 or device not in list)
        """
        if not self._license_key:
            return False

        try:
            client = CloudClient()
            response = client.get_auth_status()

            # Check device presence in list
            my_device_id = get_device_id()
            devices = response.get("devices", {}).get("list", [])
            device_ids = [d.get("device_id") for d in devices]

            if my_device_id not in device_ids:
                # Device was revoked on server
                self._state = {"user": {"status": "revoked"}}
                self._save_to_cache()
                raise LicenseRevokedError("This device is no longer authorized")

            # Success - update state with server response
            self._state = response
            self._state["_meta"] = {
                "last_validated": datetime.now(timezone.utc).isoformat()
            }
            self._save_to_cache()
            return True

        except CloudAuthError as e:
            # 401 - User not registered
            if e.status_code == 401:
                self._state = {}
                self._delete_cache()
                raise LicenseNotFoundError(
                    "License not activated on this device. Please register."
                )

            # 403 - Expired or revoked
            if e.status_code == 403:
                error_msg = str(e).lower()
                if "expired" in error_msg:
                    self._state["user"] = self._state.get("user", {})
                    self._state["user"]["status"] = "expired"
                    self._save_to_cache()
                    raise LicenseExpiredError("License has expired")
                else:
                    self._state["user"] = self._state.get("user", {})
                    self._state["user"]["status"] = "revoked"
                    self._save_to_cache()
                    raise LicenseRevokedError("License has been revoked")

            raise LicenseError(str(e))

        except CloudNetworkError:
            # Server unreachable - return False to indicate grace period applies
            return False

    def register(self, license_key: str, device_name: str) -> dict[str, Any]:
        """
        Register device with license key.

        POST /auth/register

        Args:
            license_key: Valid Polar.sh license key
            device_name: Human-readable device name

        Returns:
            Server response with user, customer, and devices info

        Raises:
            CloudAuthError: Invalid license key or signature
            CloudError: Other registration errors
        """
        device_id = get_device_id()

        client = CloudClient()
        response = client.register(
            license_key=license_key,
            device_id=device_id,
            device_name=device_name,
        )

        # Save license key to config
        config = UserConfig()
        config.licenseKey = license_key
        self._license_key = license_key

        # Update in-memory state
        self._state = response
        self._state["_meta"] = {
            "last_validated": datetime.now(timezone.utc).isoformat()
        }
        self._save_to_cache()

        return response

    def deactivate(self) -> None:
        """
        Deactivate the license on this device.

        Clears local state and removes cache file.
        Does NOT revoke from server (user can do that separately).
        """
        # Clear config
        config = UserConfig()
        config.licenseKey = ""
        self._license_key = ""

        # Clear state
        self._state = {}
        self._delete_cache()

    def get_devices(self) -> list[dict[str, Any]]:
        """
        Get list of devices on the license.

        Returns:
            List of device dicts with device_id, device_name, current
        """
        return self._state.get("devices", {}).get("list", [])

    def get_license_info(self) -> dict[str, Any] | None:
        """
        Get license information for display.

        Returns:
            Dict with license_type, status, expires_at, customer info
            or None if not registered
        """
        if not self._state or "user" not in self._state:
            return None

        user = self._state.get("user", {})
        customer = self._state.get("customer", {})
        devices = self._state.get("devices", {})
        meta = self._state.get("_meta", {})

        return {
            "license_type": user.get("license_type"),
            "status": user.get("status"),
            "expires_at": user.get("expires_at"),
            "customer_email": customer.get("email"),
            "customer_name": customer.get("name"),
            "device_count": devices.get("active", 0),
            "device_limit": devices.get("limit", 3),
            "last_validated": meta.get("last_validated"),
        }
