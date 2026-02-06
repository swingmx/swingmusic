from dataclasses import asdict
from typing import Any
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from swingmusic.api.auth import admin_required

from swingmusic.db.userdata import PluginTable
from swingmusic.lib.cloud import CloudAuthError, CloudError
from swingmusic.lib.index import index_everything
from swingmusic.lib.license import LicenseManager, LicenseError
from swingmusic.config import UserConfig
from swingmusic.store.general import GeneralStore
from swingmusic.settings import Metadata
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.hardware_id import get_device_id, get_device_name
from swingmusic.utils.paths import normalize_paths

bp_tag = Tag(name="Settings", description="Customize stuff")
api = APIBlueprint("settings", __name__, url_prefix="/notsettings", abp_tags=[bp_tag])


def get_child_dirs(parent: str, children: list[str]):
    """Returns child directories in a list, given a parent directory"""

    return [_dir for _dir in children if _dir.startswith(parent) and _dir != parent]


class AddRootDirsBody(BaseModel):
    new_dirs: list[str] = Field(
        description="The new directories to add",
        example=["/home/user/Music", "/home/user/Downloads"],
    )
    removed: list[str] = Field(
        description="The directories to remove",
        example=["/home/user/Downloads"],
    )


@api.post("/add-root-dirs")
@admin_required()
def add_root_dirs(body: AddRootDirsBody):
    """
    Add custom root directories to the database.
    """
    new_dirs = body.new_dirs
    removed_dirs = body.removed

    config = UserConfig()
    db_dirs = [*config.rootDirs]

    for dir in removed_dirs:
        try:
            db_dirs.remove(dir)
        except ValueError:
            pass

    final_paths = [*db_dirs, *new_dirs]
    config.rootDirs = normalize_paths(final_paths)
    config.save()

    index_everything()
    GeneralStore.root_dirs_set = True

    return {"root_dirs": config.rootDirs}


@api.get("/get-root-dirs")
def get_root_dirs():
    """
    Get root directories
    """
    return {"dirs": UserConfig().rootDirs}


@api.get("")
def get_all_settings():
    """
    Get all settings
    """
    config = asdict(UserConfig())

    # Convert sets to lists for JSON serialization
    for key, value in config.items():
        if isinstance(value, set):
            config[key] = sorted(list(value))

    config["plugins"] = [p for p in PluginTable.get_all()]
    config["version"] = Metadata.version

    if config["version"] == "0.0.0":
        # fallback to version.txt (useful for docker builds)
        config["version"] = open("version.txt", "r").read().strip()

    # only return lastfmSessionKey for the current user
    current_user = get_current_userid()
    config["lastfmSessionKey"] = config["lastfmSessionKeys"].get(str(current_user), "")
    del config["lastfmSessionKeys"]

    # remove license info if user is not admin
    # if "admin" not in UserTable.get_by_id(current_user).roles:
    del config["licenseKey"]

    # add device name to config
    config["deviceName"] = get_device_name()
    config["deviceId"] = get_device_id()

    return config


class SetSettingBody(BaseModel):
    key: str = Field(
        description="The setting key",
        example="artist_separators",
    )
    value: Any = Field(
        description="The setting value",
        example=",",
    )


@api.get("/trigger-scan")
def trigger_scan():
    """
    Triggers scan for new music
    """
    index_everything()
    return {"msg": "Scan triggered!"}


class UpdateConfigBody(BaseModel):
    key: str = Field(
        description="The setting key",
        example="usersOnLogin",
    )
    value: Any = Field(
        description="The setting value",
        example=False,
    )


@api.put("/update")
@admin_required()
def update_config(body: UpdateConfigBody):
    """
    Update the config file
    """
    config = UserConfig()
    if body.key == "artistSeparators":
        body.value = body.value.split(",")

    setattr(config, body.key, body.value)

    # INFO: Rebuild stores when these settings are updated
    reset_stores_lists = {
        "artistSeparators",
        "artistSplitIgnoreList",
        "removeProdBy",
        "removeRemasterInfo",
        "mergeAlbums",
        "cleanAlbumTitle",
        "showAlbumsAsSingles",
    }

    if body.key in reset_stores_lists:
        index_everything()

    return {
        "msg": "Config updated!",
    }


# =============================================================================
# License Management
# =============================================================================


class RegisterLicenseBody(BaseModel):
    license_key: str = Field(
        description="The Polar.sh license key",
        example="XXXX-XXXX-XXXX-XXXX",
    )
    device_name: str = Field(
        description="Human-readable device name",
        example="MacBook Pro",
    )


@api.post("/license/register")
@admin_required()
def register_license(body: RegisterLicenseBody):
    """
    Register this device with a license key.

    Activates premium features for this device.
    Each license supports up to 3 devices.
    """
    try:
        manager = LicenseManager()
        result = manager.register(body.license_key, body.device_name)

        return {
            "msg": "License activated successfully",
            "license": result.get("user"),
            "customer": result.get("customer"),
            "devices": result.get("devices"),
        }
    except CloudAuthError as e:
        return {"error": str(e)}, e.status_code or 400
    except CloudError as e:
        return {"error": str(e)}, e.status_code or 500


@api.get("/license/status")
@admin_required()
def get_license_status():
    """
    Get current license status.

    Returns license info if registered, or null if not.
    """
    manager = LicenseManager()
    info = manager.get_license_info()

    if not info:
        return {"error": "No license found"}, 404

    return info, 200


# @api.delete("/license/deactivate")
# @admin_required()
# def deactivate_license():
#     """
#     Deactivate the license on this device.

#     Clears local license state. Does not revoke the device from the server.
#     """
#     manager = LicenseManager()
#     manager.deactivate()

#     return {"msg": "License deactivated"}


class DeviceIdPath(BaseModel):
    device_id: str = Field(
        description="The device ID to revoke",
        example="a1b2c3d4e5f67890",
    )


@api.delete("/license/device/<device_id>")
@admin_required()
def revoke_device(path: DeviceIdPath):
    """
    Revoke a device from the license.

    Can revoke any device on your license, including yourself.
    """
    device_id = path.device_id

    try:
        from swingmusic.lib.cloud import CloudClient

        client = CloudClient()
        result = client.revoke_device(device_id)

        # if the device is the current device, deactivate the license
        if device_id == get_device_id():
            manager = LicenseManager()
            manager.deactivate()

        # Re-validate to update local state
        manager = LicenseManager()
        try:
            manager.validate()
        except LicenseError:
            pass  # State already updated

        return {
            "msg": "Device revoked",
            "revoked": result.get("revoked"),
            "devices": result.get("devices"),
        }
    except CloudAuthError as e:
        return {"error": str(e)}, e.status_code or 400
    except CloudError as e:
        return {"error": str(e)}, e.status_code or 500
