from dataclasses import asdict
from typing import Any
from flask import request
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from app.api.auth import admin_required

from app.db.sqlite.plugins import PluginsMethods as pdb
from app.db.sqlite.tracks import SQLiteTrackMethods as trackdb
from app.db.userdata import PluginTable
from app.lib.index import index_everything
from app.lib.watchdogg import Watcher as WatchDog
from app.logger import log
from app.settings import Info, Paths, SessionVarKeys
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.generators import get_random_str
from app.utils.threading import background
from app.config import UserConfig

bp_tag = Tag(name="Settings", description="Customize stuff")
api = APIBlueprint("settings", __name__, url_prefix="/notsettings", abp_tags=[bp_tag])


def get_child_dirs(parent: str, children: list[str]):
    """Returns child directories in a list, given a parent directory"""

    return [_dir for _dir in children if _dir.startswith(parent) and _dir != parent]


def reload_everything(instance_key: str):
    """
    Reloads all stores using the current database items
    """
    try:
        TrackStore.load_all_tracks(instance_key)
    except Exception as e:
        log.error(e)

    try:
        AlbumStore.load_albums(instance_key=instance_key)
    except Exception as e:
        log.error(e)

    try:
        ArtistStore.load_artists(instance_key)
    except Exception as e:
        log.error(e)

# CHECKPOINT: TEST SETTINGS API ENDPOINTS

# @background
# def rebuild_store(db_dirs: list[str]):
#     """
#     Restarts watchdog and rebuilds the music library.
#     """
#     instance_key = get_random_str()

#     log.info("Rebuilding library...")
#     trackdb.remove_tracks_not_in_folders(db_dirs)
#     reload_everything(instance_key)

#     try:
#         populate.Populate(instance_key=instance_key)
#     except populate.PopulateCancelledError as e:
#         print(e)
#         reload_everything(instance_key)
#         return

#     WatchDog().restart()

#     log.info("Rebuilding library... ✅")


# # I freaking don't know what this function does anymore
# def finalize(new_: list[str], removed_: list[str], db_dirs_: list[str]):
#     """
#     Params:
#         new_: will be added to the database
#         removed_: will be removed from the database
#         db_dirs_: will be used to remove tracks that
#         are outside these directories from the database and store.
#     """
#     sdb.remove_root_dirs(removed_)
#     sdb.add_root_dirs(new_)
#     rebuild_store(db_dirs_)


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


# maps settings to their parser flags
mapp = {
    "artist_separators": SessionVarKeys.ARTIST_SEPARATORS,
    "extract_feat": SessionVarKeys.EXTRACT_FEAT,
    "remove_prod": SessionVarKeys.REMOVE_PROD,
    "clean_album_title": SessionVarKeys.CLEAN_ALBUM_TITLE,
    "remove_remaster": SessionVarKeys.REMOVE_REMASTER_FROM_TRACK,
    "merge_albums": SessionVarKeys.MERGE_ALBUM_VERSIONS,
    "show_albums_as_singles": SessionVarKeys.SHOW_ALBUMS_AS_SINGLES,
}


@api.get("")
def get_all_settings():
    """
    Get all settings
    """
    config = asdict(UserConfig())
    plugins = PluginTable.get_all()
    config["plugins"] = plugins
    config["version"] = Info.SWINGMUSIC_APP_VERSION

    return config


@background
def reload_all_for_set_setting():
    reload_everything(get_random_str())


class SetSettingBody(BaseModel):
    key: str = Field(
        description="The setting key",
        example="artist_separators",
    )
    value: Any = Field(
        description="The setting value",
        example=",",
    )


@api.post("/set")
@admin_required()
def set_setting(body: SetSettingBody):
    """
    Set a setting.
    """
    key = body.key
    value = body.value

    if key is None or value is None or key == "root_dirs":
        return {"msg": "Invalid arguments!"}, 400

    root_dir = sdb.get_root_dirs()

    if not root_dir:
        return {"msg": "No root directories set!"}, 400

    if key not in mapp:
        return {"msg": "Invalid key!"}, 400

    sdb.set_setting(key, value)

    flag = mapp[key]

    if key == "artist_separators":
        value = str(value).split(",")
        value = set(value)

    reload_all_for_set_setting()

    # if value is a set, convert it to a string
    # (artist_separators)
    if type(value) == set:
        value = ",".join(value)

    return {"result": value}


@background
def run_populate():
    # populate.Populate(instance_key=get_random_str())
    pass


@api.get("/trigger-scan")
def trigger_scan():
    """
    Triggers scan for new music
    """
    run_populate()

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
    setattr(config, body.key, body.value)

    return {
        "msg": "Config updated!",
    }
