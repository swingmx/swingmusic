from flask import Blueprint, request
from app.db.sqlite.settings import SettingsSQLMethods as sdb

settingsbp = Blueprint("settings", __name__, url_prefix="/")


@settingsbp.route("/settings/add-root-dirs", methods=["POST"])
def add_root_dirs():
    """
    Add custom root directories to the database.
    """
    msg = {"msg": "Failed! No directories were given."}

    data = request.get_json()

    if data is None:
        return msg, 400

    try:
        new_dirs = data["new_dirs"]
        removed_dirs = data["removed"]
    except KeyError:
        return msg, 400

    sdb.add_root_dirs(new_dirs)
    sdb.remove_root_dirs(removed_dirs)

    return {"msg": "Added root directories to the database."}


@settingsbp.route("/settings/get-root-dirs", methods=["GET"])
def get_root_dirs():
    """
    Get custom root directories from the database.
    """
    dirs = sdb.get_root_dirs()

    return {"dirs": dirs}


# CURRENTLY UNUSED ROUTE 👇
@settingsbp.route("/settings/remove-root-dirs", methods=["POST"])
def remove_root_dirs():
    """
    Remove custom root directories from the database.
    """
    msg = {"msg": "Failed! No directories were given."}

    data = request.get_json()

    if data is None:
        return msg, 400

    try:
        dirs = data["dirs"]
    except KeyError:
        return msg, 400

    sdb.remove_root_dirs(dirs)

    return {"msg": "Removed root directories from the database."}
