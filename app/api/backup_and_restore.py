from dataclasses import asdict
import json
from pathlib import Path
import shutil
from time import time
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from app.api.auth import admin_required

from app.db.userdata import FavoritesTable, PlaylistTable, ScrobbleTable
from app.settings import Paths

bp_tag = Tag(name="Backup and Restore", description="Backup and Restore")
api = APIBlueprint("backup_and_restore", __name__, url_prefix="/", abp_tags=[bp_tag])


@api.post("/backup")
@admin_required()
def backup():
    """
    Create a backup file of your favorites, playlists and scrobble data.
    """
    backup_dir = Path(Paths.get_app_dir()) / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_name = f"backup.{int(time())}"
    backup_file = backup_dir / f"{backup_name}.json"

    # INFO: Image folder for playlist images
    img_folder = backup_dir / "images" / backup_name
    img_folder.mkdir(parents=True, exist_ok=True)

    favorites = FavoritesTable.get_all()
    favorites = [asdict(entry) for entry in favorites]

    scrobbles = ScrobbleTable.get_all(start=0)
    scrobbles = [asdict(entry) for entry in scrobbles]

    # SECTION: Playlists
    playlists = PlaylistTable.get_all()
    playlist_dicts = []

    for entry in playlists:
        playlist = asdict(entry)
        for key in ["_last_updated", "has_image", "images", "duration", "count"]:
            del playlist[key]

        playlist_dicts.append(playlist)

        # copy images
        if playlist["thumb"]:
            img_path = Path(Paths.get_playlist_img_path()) / playlist["thumb"]
            shutil.copy(img_path, img_folder / playlist["thumb"])

    # !SECTION

    data = {
        "favorites": favorites,
        "scrobbles": scrobbles,
        "playlists": playlist_dicts,
    }

    with open(backup_file, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "msg": "Backup created",
        "data_path": str(backup_file),
        "images_path": str(img_folder),
    }, 200


@api.post("/restore")
@admin_required()
def restore():
    """
    Restore your favorites, playlists and scrobble data from a backup file.
    """
    return {"msg": "Restore"}
