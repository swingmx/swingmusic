from dataclasses import asdict
from typing import Any
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from swingmusic.api.auth import admin_required

from swingmusic.db.userdata import PluginTable
from swingmusic.lib.index import index_everything
from swingmusic.settings import Info
from swingmusic.config import UserConfig
from swingmusic.utils.auth import get_current_userid

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
    db_dirs = config.rootDirs
    home = "$home"

    db_home = any([d == home for d in db_dirs])  # if $home is in db
    incoming_home = any([d == home for d in new_dirs])  # if $home is in incoming

    # handle $home case
    if db_home and incoming_home:
        return {"msg": "Not changed!"}, 304

    # if $home is the current root dir or the incoming root dir
    # is $home, remove all root dirs
    if db_home or incoming_home:
        config.rootDirs = []

    if incoming_home:
        config.rootDirs = [home]
        index_everything()
        return {"root_dirs": [home]}

    # ---

    for _dir in new_dirs:
        children = get_child_dirs(_dir, db_dirs)
        removed_dirs.extend(children)

    for _dir in removed_dirs:
        try:
            db_dirs.remove(_dir)
        except ValueError:
            pass

    db_dirs.extend(new_dirs)
    config.rootDirs = [dir_ for dir_ in db_dirs if dir_ != home]

    index_everything()
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
    config["plugins"] = [p for p in PluginTable.get_all()]
    config["version"] = Info.SWINGMUSIC_APP_VERSION

    # hide lastfmSessionKeys for other users
    current_user = get_current_userid()
    config["lastfmSessionKey"] = config["lastfmSessionKeys"].get(str(current_user), "")
    del config["lastfmSessionKeys"]

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
