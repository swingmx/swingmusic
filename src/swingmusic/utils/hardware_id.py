"""
Cross-platform hardware identification for device fingerprinting.
"""

import uuid
import platform
import subprocess
from functools import lru_cache

from swingmusic.utils.hashing import create_hash


def _run_command(args: list[str], timeout: int = 5) -> str | None:
    """
    Run a subprocess command and return stdout, or None on failure.
    """
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def _get_macos_hardware_id() -> str | None:
    """
    Get Hardware UUID on macOS via system_profiler.
    """
    output = _run_command(["system_profiler", "SPHardwareDataType"])
    if output:
        for line in output.split("\n"):
            if "Hardware UUID" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    return parts[1].strip()
    return None


def _get_linux_machine_id() -> str | None:
    """
    Get machine-id on Linux from /etc/machine-id or /var/lib/dbus/machine-id.
    """
    for path in ["/etc/machine-id", "/var/lib/dbus/machine-id"]:
        try:
            with open(path, "r") as f:
                machine_id = f.read().strip()
                if machine_id:
                    return machine_id
        except (FileNotFoundError, PermissionError, OSError):
            continue
    return None


def _get_windows_cpu_id() -> str | None:
    """
    Get CPU ProcessorId on Windows via wmic.
    """
    output = _run_command(["wmic", "cpu", "get", "ProcessorId"])
    if output:
        lines = output.split("\n")
        if len(lines) >= 2:
            cpu_id = lines[1].strip()
            if cpu_id:
                return cpu_id
    return None


def _get_freebsd_host_uuid() -> str | None:
    """
    Get host UUID on FreeBSD via sysctl or kenv.
    """
    # Try kern.hostuuid first
    output = _run_command(["sysctl", "-n", "kern.hostuuid"])
    if output:
        return output

    # Fallback to SMBIOS system UUID
    output = _run_command(["kenv", "smbios.system.uuid"])
    if output:
        return output

    return None


def _get_openbsd_hw_uuid() -> str | None:
    """
    Get hardware UUID on OpenBSD via sysctl.
    """
    output = _run_command(["sysctl", "-n", "hw.uuid"])
    return output if output else None


def _get_netbsd_dmi_uuid() -> str | None:
    """
    Get DMI system UUID on NetBSD via sysctl.
    """
    output = _run_command(["sysctl", "-n", "machdep.dmi.system-uuid"])
    return output if output else None


def _get_mac_address() -> str:
    """
    Get MAC address as fallback identifier.
    """
    return str(uuid.getnode())


@lru_cache(maxsize=1)
def get_raw_hardware_id() -> str:
    """
    Get a raw hardware identifier for the current platform.

    Returns the most stable hardware identifier available:
    - macOS: Hardware UUID
    - Linux: /etc/machine-id
    - Windows: CPU ProcessorId
    - FreeBSD: kern.hostuuid
    - OpenBSD: hw.uuid
    - NetBSD: machdep.dmi.system-uuid
    - Fallback: MAC address

    The result is cached for the lifetime of the process.
    """
    system = platform.system()
    hw_id = None

    if system == "Darwin":
        hw_id = _get_macos_hardware_id()

    elif system == "Linux":
        hw_id = _get_linux_machine_id()

    elif system == "Windows":
        hw_id = _get_windows_cpu_id()

    elif system == "FreeBSD":
        hw_id = _get_freebsd_host_uuid()

    elif system == "OpenBSD":
        hw_id = _get_openbsd_hw_uuid()

    elif system == "NetBSD":
        hw_id = _get_netbsd_dmi_uuid()

    # Fallback to MAC address if platform-specific method failed
    if not hw_id:
        hw_id = _get_mac_address()

    return hw_id


@lru_cache(maxsize=1)
def get_device_id() -> str:
    """
    Get a hashed device identifier suitable for license activation.

    Returns a hex string that uniquely identifies this device.
    """
    raw_id = get_raw_hardware_id()
    return create_hash(raw_id)


def get_device_name() -> str:
    """
    Get a human-readable device name for display purposes.

    Returns the hostname or a fallback description.
    """
    try:
        hostname = platform.node()
        if hostname:
            return hostname
    except Exception:
        pass

    return f"{platform.system()} Device"
