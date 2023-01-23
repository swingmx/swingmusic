from flask import Blueprint, request
from app import settings

from app.db.sqlite.settings import SettingsSQLMethods as sdb
from app.lib import populate
from app.logger import log

from app.db.store import Store
from app.utils import background

api = Blueprint("settings", __name__, url_prefix="/")


def get_child_dirs(parent: str, children: list[str]):
    """Returns child directories in a list, given a parent directory"""

    return [dir for dir in children if dir.startswith(parent) and dir != parent]


@background
def rebuild_store(db_dirs: list[str]):
    log.info("Rebuilding library...")
    Store.remove_tracks_by_dir_except(db_dirs)

    Store.load_all_tracks()
    Store.process_folders()
    Store.load_albums()
    Store.load_artists()

    populate.Populate()

    log.info("Rebuilding library... ✅")


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

    def finalize(new_dirs: list[str], removed_dirs: list[str], db_dirs: list[str]):
        sdb.remove_root_dirs(removed_dirs)
        sdb.add_root_dirs(new_dirs)
        rebuild_store(db_dirs)

    # ---
    db_dirs = sdb.get_root_dirs()

    if db_dirs[0] == "$home" and new_dirs[0] == "$home".strip():
        return {"msg": "Not changed!"}

    if db_dirs[0] == "$home":
        sdb.remove_root_dirs(db_dirs)

    try:
        if new_dirs[0] == "$home":
            finalize(["$home"], db_dirs, [settings.USER_HOME_DIR])

            return {"msg": "Updated!"}
    except IndexError:
        pass

    for _dir in new_dirs:
        children = get_child_dirs(_dir, db_dirs)
        removed_dirs.extend(children)
    # ---

    for _dir in removed_dirs:
        try:
            db_dirs.remove(_dir)
        except ValueError:
            pass

    db_dirs.extend(new_dirs)

    finalize(new_dirs, removed_dirs, db_dirs)

    return {"msg": "Updated!"}


@api.route("/settings/get-root-dirs", methods=["GET"])
def get_root_dirs():
    """
    Get custom root directories from the database.
    """
    dirs = sdb.get_root_dirs()

    return {"dirs": dirs}
