"""
Device type detection for license tracking.

Detects whether the software is running on a laptop, desktop, server, or handheld device.
Used to display appropriate icons in the frontend license settings.
"""

import os
import platform
import subprocess
from enum import Enum
from pathlib import Path
from functools import lru_cache


class DeviceType(str, Enum):
    """Device types for license tracking and frontend icon display."""

    LAPTOP = "laptop"
    DESKTOP = "desktop"
    SERVER = "server"
    HANDHELD = "handheld"


# DMI chassis type codes (SMBIOS specification)
# https://www.dmtf.org/sites/default/files/standards/documents/DSP0134_3.4.0.pdf
LAPTOP_CHASSIS_TYPES = {
    8,
    9,
    10,
    11,
    14,
    31,
}  # Portable, Laptop, Notebook, Hand Held, Sub Notebook, Convertible
DESKTOP_CHASSIS_TYPES = {
    3,
    4,
    5,
    6,
    7,
    13,
    15,
    16,
    35,
    36,
}  # Desktop, Low Profile, Pizza Box, Mini Tower, Tower, All In One, Space-saving, Lunch Box, Mini PC, Stick PC
SERVER_CHASSIS_TYPES = {
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
}  # Main Server Chassis, Expansion Chassis, Sub Chassis, Bus Expansion, Peripheral, RAID, Rack Mount, Sealed-case PC, Multi-system


def _is_termux() -> bool:
    """Check if running in Termux (Android terminal emulator)."""
    return bool(os.environ.get("TERMUX_VERSION") or os.environ.get("TERMUX_APP_PID"))


def _is_android() -> bool:
    """Check if running on Android."""
    return bool(
        os.environ.get("ANDROID_ROOT")
        or os.environ.get("ANDROID_DATA")
        or Path("/system/build.prop").exists()
    )


def _is_container() -> bool:
    """Check if running inside a container (Docker, Podman, LXC, etc.)."""
    # Docker
    if Path("/.dockerenv").exists():
        return True

    # Podman
    if Path("/run/.containerenv").exists():
        return True

    # Check cgroups for container signatures
    try:
        cgroup_path = Path("/proc/1/cgroup")
        if cgroup_path.exists():
            content = cgroup_path.read_text()
            if any(
                sig in content for sig in ["docker", "kubepods", "lxc", "containerd"]
            ):
                return True
    except (PermissionError, OSError):
        pass

    # Check for container environment variables
    if os.environ.get("container") or os.environ.get("KUBERNETES_SERVICE_HOST"):
        return True

    return False


def _is_vm_linux() -> bool:
    """Check if running in a VM on Linux."""
    # Check for hypervisor
    if Path("/sys/hypervisor/type").exists():
        return True

    # Check DMI for VM signatures
    dmi_paths = [
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/board_vendor",
    ]
    vm_signatures = [
        "virtualbox",
        "vmware",
        "qemu",
        "kvm",
        "xen",
        "hyper-v",
        "parallels",
        "bochs",
        "virtual machine",
        "innotek",
    ]

    for dmi_path in dmi_paths:
        try:
            path = Path(dmi_path)
            if path.exists():
                content = path.read_text().lower()
                if any(sig in content for sig in vm_signatures):
                    return True
        except (PermissionError, OSError):
            pass

    return False


def _is_vm_macos() -> bool:
    """Check if running in a VM on macOS."""
    try:
        result = subprocess.run(
            ["sysctl", "-n", "kern.hv_vmm_present"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() == "1"
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _is_vm_windows() -> bool:
    """Check if running in a VM on Windows using WMI."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "(Get-WmiObject -Class Win32_ComputerSystem).Model",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        model = result.stdout.lower()
        vm_signatures = [
            "virtual",
            "vmware",
            "virtualbox",
            "qemu",
            "xen",
            "hyper-v",
            "kvm",
        ]
        if any(sig in model for sig in vm_signatures):
            return True
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _is_vm_freebsd() -> bool:
    """Check if running in a VM on FreeBSD."""
    try:
        result = subprocess.run(
            ["sysctl", "-n", "kern.vm_guest"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        guest = result.stdout.strip().lower()
        return guest != "none" and guest != ""
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _is_vm() -> bool:
    """Check if running in a virtual machine."""
    system = platform.system().lower()

    if system == "linux":
        return _is_vm_linux()
    elif system == "darwin":
        return _is_vm_macos()
    elif system == "windows":
        return _is_vm_windows()
    elif system == "freebsd":
        return _is_vm_freebsd()

    return False


def _has_battery_linux() -> bool:
    """Check for battery presence on Linux."""
    power_supply_path = Path("/sys/class/power_supply")
    if not power_supply_path.exists():
        return False

    for supply in power_supply_path.iterdir():
        type_file = supply / "type"
        try:
            if (
                type_file.exists()
                and type_file.read_text().strip().lower() == "battery"
            ):
                # Verify it's a real battery, not just an entry
                status_file = supply / "status"
                if status_file.exists():
                    return True
        except (PermissionError, OSError):
            pass

    return False


def _has_battery_macos() -> bool:
    """Check for battery presence on macOS."""
    try:
        result = subprocess.run(
            ["pmset", "-g", "batt"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = result.stdout.lower()
        # If there's battery info, it will mention percentage or "battery"
        return "battery" in output and "no battery" not in output
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _has_battery_windows() -> bool:
    """Check for battery presence on Windows."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "(Get-WmiObject -Class Win32_Battery).BatteryStatus",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # If there's a battery, this will return a status number
        return bool(result.stdout.strip())
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _has_battery_freebsd() -> bool:
    """Check for battery presence on FreeBSD."""
    try:
        result = subprocess.run(
            ["acpiconf", "-i", "0"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0 and "State:" in result.stdout
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return False


def _has_battery() -> bool:
    """Check if device has a battery (indicates laptop/portable)."""
    system = platform.system().lower()

    if system == "linux":
        return _has_battery_linux()
    elif system == "darwin":
        return _has_battery_macos()
    elif system == "windows":
        return _has_battery_windows()
    elif system == "freebsd":
        return _has_battery_freebsd()

    return False


def _get_chassis_type_linux() -> int | None:
    """Get chassis type from DMI on Linux."""
    chassis_path = Path("/sys/class/dmi/id/chassis_type")
    try:
        if chassis_path.exists():
            return int(chassis_path.read_text().strip())
    except (ValueError, PermissionError, OSError):
        pass

    return None


def _get_chassis_type_windows() -> int | None:
    """Get chassis type from WMI on Windows."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-Command",
                "(Get-WmiObject -Class Win32_SystemEnclosure).ChassisTypes[0]",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.stdout.strip():
            return int(result.stdout.strip())
    except (ValueError, subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return None


def _detect_macos_form_factor() -> DeviceType | None:
    """Detect form factor on macOS using system_profiler."""
    try:
        result = subprocess.run(
            ["system_profiler", "SPHardwareDataType"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout.lower()

        # Check model identifier
        if "macbook" in output:
            return DeviceType.LAPTOP
        elif any(
            name in output for name in ["imac", "mac mini", "mac studio", "mac pro"]
        ):
            return DeviceType.DESKTOP
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return None


def _detect_from_chassis_type(chassis_type: int | None) -> DeviceType | None:
    """Map chassis type to device type."""
    if chassis_type is None:
        return None

    if chassis_type in LAPTOP_CHASSIS_TYPES:
        return DeviceType.LAPTOP
    elif chassis_type in DESKTOP_CHASSIS_TYPES:
        return DeviceType.DESKTOP
    elif chassis_type in SERVER_CHASSIS_TYPES:
        return DeviceType.SERVER

    return None


@lru_cache(maxsize=1)
def detect_device_type() -> DeviceType:
    """
    Detect the type of device the software is running on.

    Detection priority:
    1. Android/Termux → handheld
    2. Container (Docker, Podman, LXC) → server
    3. Virtual machine → server
    4. Battery present → laptop
    5. Chassis type (DMI/WMI) → laptop/desktop/server
    6. macOS form factor → laptop/desktop
    7. Default → server

    Returns:
        DeviceType: One of LAPTOP, DESKTOP, SERVER, or HANDHELD
    """
    # 1. Check for Android/Termux (handheld)
    if _is_termux() or _is_android():
        return DeviceType.HANDHELD

    # 2. Check for container (server)
    if _is_container():
        return DeviceType.SERVER

    # 3. Check for VM (server)
    if _is_vm():
        return DeviceType.SERVER

    # 4. Check for battery (laptop)
    if _has_battery():
        return DeviceType.LAPTOP

    # 5. Check chassis type
    system = platform.system().lower()

    if system == "linux":
        chassis_type = _get_chassis_type_linux()
        device_type = _detect_from_chassis_type(chassis_type)
        if device_type:
            return device_type

    elif system == "windows":
        chassis_type = _get_chassis_type_windows()
        device_type = _detect_from_chassis_type(chassis_type)
        if device_type:
            return device_type

    elif system == "darwin":
        # 6. macOS-specific detection
        device_type = _detect_macos_form_factor()
        if device_type:
            return device_type

    # 7. Default to server
    return DeviceType.SERVER


def get_device_type() -> str:
    """
    Get the device type as a string for API payloads.

    Returns:
        str: One of "laptop", "desktop", "server", or "handheld"
    """
    return detect_device_type().value
