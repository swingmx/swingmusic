from flask import Blueprint, request
from app import settings

from app.logger import log
from app.lib import populate
from app.lib.watchdogg import Watcher as WatchDog
from app.db.sqlite.settings import SettingsSQLMethods as sdb
from app.utils.generators import get_random_str
from app.utils.threading import background

from app.store.albums import AlbumStore
from app.store.tracks import TrackStore
from app.store.artists import ArtistStore

api = Blueprint("settings", __name__, url_prefix="/")


def get_child_dirs(parent: str, children: list[str]):
    """Returns child directories in a list, given a parent directory"""

    return [_dir for _dir in children if _dir.startswith(parent) and _dir != parent]


def reload_everything():
    """
    Reloads all stores using the current database items
    """
    TrackStore.load_all_tracks()
    AlbumStore.load_albums()
    ArtistStore.load_artists()


@background
def rebuild_store(db_dirs: list[str]):
    """
    Restarts the watchdog and rebuilds the music library.
    """
    log.info("Rebuilding library...")
    TrackStore.remove_tracks_by_dir_except(db_dirs)
    reload_everything()

    key = get_random_str()
    try:
        populate.Populate(key=key)
    except populate.PopulateCancelledError:
        reload_everything()
        return

    WatchDog().restart()

    log.info("Rebuilding library... ✅")


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
        finalize([_h], [], [settings.Paths.USER_HOME_DIR])
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
