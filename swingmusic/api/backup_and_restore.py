from dataclasses import asdict
import json
import os
from pathlib import Path
from pprint import pprint
import shutil
from time import time
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from swingmusic.api.auth import admin_required

from swingmusic.db.userdata import FavoritesTable, PlaylistTable, ScrobbleTable
from swingmusic.lib.index import index_everything
from swingmusic.settings import Paths
from datetime import datetime
from swingmusic.utils.dates import timestamp_to_time_passed

from pydantic import BaseModel, Field
from typing import Optional

bp_tag = Tag(name="Backup and Restore", description="Backup and Restore")
api = APIBlueprint(
    "backup_and_restore", __name__, url_prefix="/backup", abp_tags=[bp_tag]
)


@api.post("/create")
@admin_required()
def backup():
    """
    Create a backup file of your favorites, playlists and scrobble data.
    """
    backup_name = f"backup.{int(time())}"
    backup_dir = Path("~").expanduser() / "swingmusic.backup" / backup_name
    backup_dir.mkdir(parents=True, exist_ok=True)

    backup_file = backup_dir / "data.json"
    img_folder = backup_dir / "images"
    img_folder_created = img_folder.exists()

    favorites = FavoritesTable.get_all()
    favorites = [asdict(entry) for entry in favorites]

    scrobbles = ScrobbleTable.get_all(start=0)
    scrobbles = [asdict(entry) for entry in scrobbles]

    for scrobble in scrobbles:
        del scrobble["id"]

    # SECTION: Playlists
    playlists = PlaylistTable.get_all()
    playlist_dicts = []

    for entry in playlists:
        playlist = asdict(entry)
        for key in [
            "id",
            "_last_updated",
            "has_image",
            "images",
            "duration",
            "count",
            "pinned",
            "thumb",
        ]:
            del playlist[key]

        playlist_dicts.append(playlist)

        # copy images
        img_path = Path(Paths.get_playlist_img_path()) / str(playlist["image"])
        if img_path.exists():
            if not img_folder_created:
                img_folder.mkdir(parents=True)
                img_folder_created = True

            shutil.copy(img_path, img_folder / playlist["image"])

    # !SECTION
    data = {
        "favorites": favorites,
        "scrobbles": scrobbles,
        "playlists": playlist_dicts,
    }

    with open(backup_file, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "name": backup_name,
        "date": timestamp_to_time_passed(int(backup_name.split(".")[1])),
        "scrobbles": len(scrobbles),
        "favorites": len(favorites),
        "playlists": len(playlist_dicts),
    }, 200


class RestoreBackup:
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir
        self.backup_file = backup_dir / "data.json"
        with open(self.backup_file, "r") as f:
            self.data = json.load(f)

        self.restore_favorites(self.data["favorites"])
        self.restore_playlists(self.data["playlists"])
        self.restore_scrobbles(self.data["scrobbles"])

    def restore(self):
        pass

    def restore_favorites(self, favorites: list[dict]):
        existing_favorites = FavoritesTable.get_all()
        existing_hashes = set(fav.hash for fav in existing_favorites)
        new_favorites = [fav for fav in favorites if fav["hash"] not in existing_hashes]

        if new_favorites:
            FavoritesTable.insert_many(new_favorites)

    def restore_playlists(self, playlists: list[dict]):
        existing_playlists = PlaylistTable.get_all()
        existing_names = set(playlist.name for playlist in existing_playlists)
        new_playlists = [
            playlist for playlist in playlists if playlist["name"] not in existing_names
        ]

        if new_playlists:
            PlaylistTable.insert_many(new_playlists)

    def restore_scrobbles(self, scrobbles: list[dict]):
        existing_scrobbles = ScrobbleTable.get_all(0)
        existing_hashes = set(
            f"{scrobble.trackhash}.{scrobble.timestamp}"
            for scrobble in existing_scrobbles
        )
        new_scrobbles = [
            scrobble
            for scrobble in scrobbles
            if f"{scrobble['trackhash']}.{scrobble['timestamp']}" not in existing_hashes
        ]

        if new_scrobbles:
            ScrobbleTable.insert_many(new_scrobbles)


class RestoreBackupBody(BaseModel):
    backup_dir: Optional[str] = Field(
        default=None,
        description="The name of the backup directory to restore from. If not provided, all backups will be restored.",
        example="backup.1234567890",
    )


@api.post("/restore")
@admin_required()
def restore(body: RestoreBackupBody):
    """
    Restore your favorites, playlists and scrobble data from a specified backup or all backups.
    """
    backup_base_dir = Path("~").expanduser() / "swingmusic.backup"
    backups = []

    if body.backup_dir:
        # Restore from a specific backup
        specified_backup_dir = backup_base_dir / body.backup_dir
        if not specified_backup_dir.exists() or not specified_backup_dir.is_dir():
            return {"msg": f"Backup '{body.backup_dir}' not found"}, 404

        restore_backup = RestoreBackup(specified_backup_dir)
        restore_backup.restore()
        backups.append(body.backup_dir)
    else:
        # Restore from all backups
        try:
            backup_dirs = [d for d in backup_base_dir.iterdir() if d.is_dir()]
        except FileNotFoundError:
            backup_dirs = []

        if not backup_dirs:
            return {"msg": "No backups found"}, 404

        for backup_dir in sorted(backup_dirs, key=lambda x: x.name, reverse=True):
            restore_backup = RestoreBackup(backup_dir)
            restore_backup.restore()
            backups.append(backup_dir.name)

    index_everything()
    return {"msg": f"Restored successfully", "backups": backups}, 200


@api.get("/list")
@admin_required()
def list_backups():
    """
    List all backups with detailed information.
    """
    backup_dir = Path("~").expanduser() / "swingmusic.backup"
    backups = []

    entries = []
    try:
        paths = [p for p in backup_dir.iterdir() if p.is_dir()]
    except FileNotFoundError:
        paths = []

    for path in paths:
        try:
            entries.append(
                {"path": path, "timestamp": int(path.name.split(".")[1])}
            )
        except (IndexError, ValueError):
            pass

    entries = sorted(entries, key=lambda x: x["timestamp"], reverse=True)

    for entry in entries:
        backup_info = {
            "name": entry["path"].name,
            "date": timestamp_to_time_passed(entry["timestamp"]),
        }

        # Read the JSON file and count items
        json_file: Path = entry["path"] / "data.json"
        if json_file.exists():
            with json_file.open("r") as f:
                data = json.load(f)
                backup_info["scrobbles"] = len(data.get("scrobbles", []))
                backup_info["favorites"] = len(data.get("favorites", []))
                backup_info["playlists"] = len(data.get("playlists", []))
        else:
            backup_info["scrobbles"] = 0
            backup_info["favorites"] = 0
            backup_info["playlists"] = 0

        backups.append(backup_info)

    return {"backups": backups}, 200


class DeleteBackupBody(BaseModel):
    backup_dir: str = Field(
        ..., description="The name of the backup directory to delete."
    )


@api.delete("/delete")
@admin_required()
def delete_backup(body: DeleteBackupBody):
    """
    Delete a backup.
    """
    backup_dir = Path("~").expanduser() / "swingmusic.backup"
    backup_dir = backup_dir / body.backup_dir
    if not backup_dir.exists() or not backup_dir.is_dir():
        return {"msg": f"Backup '{body.backup_dir}' not found"}, 404

    shutil.rmtree(backup_dir)
    return {"msg": f"Backup '{body.backup_dir}' deleted"}, 200
