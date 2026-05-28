"""
Cross-platform hardware identification for device fingerprinting.
"""

import os
import platform
from swingmusic.utils.hashing import create_hash


def get_device_id() -> str:
    """
    Get a hashed device identifier suitable for license activation.

    Returns a hex string that uniquely identifies this device.
    """
    try:
        from swingmusic.premium.utils import get_raw_hardware_id

        raw_id = get_raw_hardware_id()
    except ImportError:
        raw_id = "unknown"

    return create_hash(raw_id)


def get_device_name() -> str:
    """
    Get a human-readable device name for display purposes.

    Reads SWINGMUSIC_DEVICE_NAME from the environment first so containerized
    deployments can supply a stable, meaningful name (the default Docker
    hostname is a random 12-hex container id that changes on every recreate).
    Falls back to the OS hostname, then a generic "{system} Device" string.
    """
    env_name = os.environ.get("SWINGMUSIC_DEVICE_NAME", "").strip()
    if env_name:
        return env_name

    try:
        hostname = platform.node()
        if hostname:
            return hostname
    except Exception:
        pass

    return f"{platform.system()} Device"
