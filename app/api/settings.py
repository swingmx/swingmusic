from flask import Blueprint, request

from app.db.sqlite.plugins import PluginsMethods as pdb
from app.db.sqlite.settings import SettingsSQLMethods as sdb
from app.lib import populate
from app.lib.watchdogg import Watcher as WatchDog
from app.logger import log
from app.settings import Keys, Paths, SessionVarKeys, set_flag
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.generators import get_random_str
from app.utils.threading import background

api = Blueprint("settings", __name__, url_prefix="")


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


@background
def rebuild_store(db_dirs: list[str]):
    """
    Restarts the watchdog and rebuilds the music library.
    """
    instance_key = get_random_str()

    log.info("Rebuilding library...")
    TrackStore.remove_tracks_by_dir_except(db_dirs)
    reload_everything(instance_key)

    try:
        populate.Populate(instance_key=instance_key)
    except populate.PopulateCancelledError:
        reload_everything(instance_key)
        return

    WatchDog().restart()

    log.info("Rebuilding library... ✅")


# I freaking don't know what this function does anymore
def finalize(new_: list[str], removed_: list[str], db_dirs_: list[str]):
    """
    Params:
        new_: will be added to the database
        removed_: will be removed from the database
        db_dirs_: will be used to remove tracks that
        are outside these directories from the database and store.
    """
    sdb.remove_root_dirs(removed_)
    sdb.add_root_dirs(new_)
    rebuild_store(db_dirs_)


@api.route("/settings/add-root-dirs", methods=["POST"])
def add_root_dirs():
    """
    Add custom root directories to the database.
    """
    msg = {"msg": "Failed! No directories were given."}

    data = request.get_json()

    if data is None:
        return msg, 400

    try:
        new_dirs: list[str] = data["new_dirs"]
        removed_dirs: list[str] = data["removed"]
    except KeyError:
        return msg, 400

    db_dirs = sdb.get_root_dirs()
    _h = "$home"

    db_home = any([d == _h for d in db_dirs])  # if $home is in db
    incoming_home = any([d == _h for d in new_dirs])  # if $home is in incoming

    # handle $home case
    if db_home and incoming_home:
        return {"msg": "Not changed!"}

    if db_home or incoming_home:
        sdb.remove_root_dirs(db_dirs)

    if incoming_home:
        finalize([_h], [], [Paths.USER_HOME_DIR])
        return {"root_dirs": [_h]}

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
    db_dirs = [dir_ for dir_ in db_dirs if dir_ != _h]

    finalize(new_dirs, removed_dirs, db_dirs)

    return {"root_dirs": db_dirs}


@api.route("/settings/get-root-dirs", methods=["GET"])
def get_root_dirs():
    """
    Get custom root directories from the database.
    """
    dirs = sdb.get_root_dirs()

    return {"dirs": dirs}


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


@api.route("/settings/", methods=["GET"])
def get_all_settings():
    """
    Get all settings from the database.
    """

    settings = sdb.get_all_settings()
    plugins = pdb.get_all_plugins()

    key_list = list(mapp.keys())
    s = {}

    for key in key_list:
        val_index = key_list.index(key)

        try:
            s[key] = settings[val_index]

            if type(s[key]) == int:
                s[key] = bool(s[key])
            if type(s[key]) == str:
                s[key] = str(s[key]).split(",")

        except IndexError:
            s[key] = None

    root_dirs = sdb.get_root_dirs()
    s["root_dirs"] = root_dirs
    s["plugins"] = plugins
    s["version"] = Keys.SWINGMUSIC_APP_VERSION

    return {
        "settings": s,
    }


@background
def reload_all_for_set_setting():
    reload_everything(get_random_str())


@api.route("/settings/set", methods=["POST"])
def set_setting():
    key = request.get_json().get("key")
    value = request.get_json().get("value")

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

    set_flag(flag, value)
    reload_all_for_set_setting()

    # if value is a set, convert it to a string
    # (artist_separators)
    if type(value) == set:
        value = ",".join(value)

    return {"result": value}


@background
def run_populate():
    populate.Populate(instance_key=get_random_str())


@api.route("/settings/trigger-scan", methods=["GET"])
def trigger_scan():
    """
    Triggers a scan.
    """
    run_populate()

    return {"msg": "Scan triggered!"}
