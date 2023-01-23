from flask import Blueprint, request

from app.db.sqlite.settings import SettingsSQLMethods as sdb

api = Blueprint("settings", __name__, url_prefix="/")


def get_child_dirs(parent: str, children: list[str]):
    """Returns child directories in a list, given a parent directory"""

    return [dir for dir in children if dir.startswith(parent)]


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

    # --- Unregister child directories ---
    db_dirs = sdb.get_root_dirs()

    for _dir in new_dirs:
        children = get_child_dirs(_dir, db_dirs)
        removed_dirs.extend(children)
    # ------------------------------------

    sdb.add_root_dirs(new_dirs)
    sdb.remove_root_dirs(removed_dirs)

    return {"msg": "Updated!"}


@api.route("/settings/get-root-dirs", methods=["GET"])
def get_root_dirs():
    """
    Get custom root directories from the database.
    """
    dirs = sdb.get_root_dirs()

    return {"dirs": dirs}
