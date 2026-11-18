"""Playlist image cleanup with synthetic files, SQLite rows and real API routes."""

import io
import json
import logging
from pathlib import Path
from types import SimpleNamespace

import pytest
from PIL import Image


@pytest.fixture
def playlists(tmp_path, monkeypatch):
    # Configure paths before importing application modules; never use a real library.
    monkeypatch.setenv("SWINGMUSIC_CONFIG_DIR", str(tmp_path))
    monkeypatch.setenv("SWINGMUSIC_CLIENT_DIR", str(tmp_path / "client"))
    from swingmusic.settings import Paths, Singleton

    monkeypatch.setattr(Singleton, "_instances", {})
    paths = Paths(config_parent=tmp_path)

    from swingmusic.db.engine import DbEngine
    from swingmusic.db import userdata
    from swingmusic.lib import playlistlib
    from swingmusic.models import playlist as playlist_model

    # Authentication is outside this component test; requests act as synthetic user 1.
    monkeypatch.setattr(userdata, "get_current_userid", lambda: 1)
    monkeypatch.setattr(playlist_model, "get_current_userid", lambda: 1)
    monkeypatch.setattr(DbEngine, "_engine", None)
    engine = DbEngine.engine
    userdata.UserTable.__table__.create(engine)
    userdata.PlaylistTable.__table__.create(engine)
    userdata.UserTable.insert_many([
        {"id": i, "username": f"test-user-{i}", "password": "unused", "roles": []}
        for i in (1, 2)
    ])

    def add(image, userid=1):
        result = userdata.PlaylistTable.insert_one({
            "name": "Synthetic playlist",
            "image": image,
            "userid": userid,
            "last_updated": "2026-01-01 00:00:00",
            "settings": {"pinned": False},
            "trackhashes": [],
        })
        return result.lastrowid

    def files(*names):
        for name in names:
            (paths.playlist_img_path / name).write_bytes(b"synthetic image fixture")

    def names():
        return {p.name for p in paths.playlist_img_path.iterdir() if p.is_file()}

    yield SimpleNamespace(
        add=add, files=files, names=names, directory=paths.playlist_img_path,
        table=userdata.PlaylistTable, lib=playlistlib,
    )
    engine.dispose()


def test_cleanup_preserves_referenced_images_and_removes_orphans(playlists):
    playlists.add("cover.webp")
    playlists.files("cover.webp", "thumb_cover.webp", "old.webp", "thumb_old.webp")

    playlists.lib.cleanup_playlist_images()

    assert playlists.names() == {"cover.webp", "thumb_cover.webp"}
    playlists.lib.cleanup_playlist_images()
    assert playlists.names() == {"cover.webp", "thumb_cover.webp"}


def test_cleanup_preserves_shared_image_until_last_reference_is_deleted(playlists):
    first = playlists.add("shared.webp")
    second = playlists.add("shared.webp")
    playlists.files("shared.webp", "thumb_shared.webp")

    playlists.table.remove_one(first)
    playlists.lib.cleanup_playlist_images()
    assert playlists.names() == {"shared.webp", "thumb_shared.webp"}

    playlists.table.remove_one(second)
    playlists.lib.cleanup_playlist_images()
    assert playlists.names() == set()


def test_cleanup_preserves_other_users_images(playlists):
    playlists.add("mine.webp")
    playlists.add("other.webp", userid=2)
    playlists.files("mine.webp", "thumb_mine.webp", "other.webp", "thumb_other.webp")

    playlists.lib.cleanup_playlist_images()

    assert playlists.names() == {
        "mine.webp", "thumb_mine.webp", "other.webp", "thumb_other.webp",
    }


@pytest.mark.parametrize("images", [[], [None], ["None"], [""], [None, "None", ""]])
def test_cleanup_without_image_references_removes_all_files(playlists, images):
    for image in images:
        playlists.add(image)
    playlists.files("orphan.webp", "thumb_orphan.webp", "None", "thumb_None")

    playlists.lib.cleanup_playlist_images()
    playlists.lib.cleanup_playlist_images()

    assert playlists.names() == set()


def test_cleanup_skips_subdirectories(playlists):
    nested = playlists.directory / "nested"
    nested.mkdir()
    sentinel = nested / "keep.webp"
    sentinel.write_bytes(b"synthetic nested fixture")
    playlists.files("orphan.webp")

    playlists.lib.cleanup_playlist_images()

    assert sentinel.read_bytes() == b"synthetic nested fixture"
    assert playlists.names() == set()


def test_cleanup_matches_full_filename_and_exact_thumbnail_prefix(playlists):
    playlists.add("thumb_cover.webp")
    playlists.files(
        "thumb_cover.webp", "thumb_thumb_cover.webp", "cover.webp",
        "thumb_cover.jpg", "xthumb_thumb_cover.webp",
    )

    playlists.lib.cleanup_playlist_images()

    assert playlists.names() == {"thumb_cover.webp", "thumb_thumb_cover.webp"}


def test_cleanup_logs_unlink_error_and_continues(playlists, monkeypatch, caplog):
    playlists.files("blocked.webp", "removable.webp")
    unlink = Path.unlink

    def failing_unlink(path, *args, **kwargs):
        if path == playlists.directory / "blocked.webp":
            raise OSError("synthetic unlink failure")
        return unlink(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", failing_unlink)
    with caplog.at_level(logging.ERROR, logger="swingmusic.lib.playlistlib"):
        playlists.lib.cleanup_playlist_images()

    assert playlists.names() == {"blocked.webp"}
    assert "could not delete file" in caplog.text
    assert "synthetic unlink failure" in caplog.text


@pytest.fixture
def client(playlists):
    from flask_openapi3 import OpenAPI
    from swingmusic.api import playlist

    app = OpenAPI(__name__)
    app.config["TESTING"] = True
    app.register_api(playlist.api)
    return app.test_client()


def test_rename_api_keeps_all_custom_covers(playlists, client):
    first = playlists.add("first.webp")
    playlists.add("second.webp")
    playlists.add("other-user.webp", userid=2)
    covers = {
        "first.webp", "thumb_first.webp", "second.webp", "thumb_second.webp",
        "other-user.webp", "thumb_other-user.webp",
    }
    playlists.files(*covers, "orphan.webp", "thumb_orphan.webp")

    response = client.put(f"/playlists/{first}/update", data={
        "name": "Renamed", "settings": json.dumps({"pinned": False}),
        "image": (io.BytesIO(b""), ""),
    })

    assert response.status_code == 200, response.get_json()
    assert playlists.table.get_by_id(first).name == "Renamed"
    assert playlists.names() == covers
    cards = client.get("/playlists").get_json()["data"]
    assert {p["image"] for p in cards} == {"first.webp", "second.webp"}
    assert all(p["has_image"] for p in cards)


def test_delete_api_removes_only_unreferenced_covers(playlists, client):
    deleted = playlists.add("deleted.webp")
    shared = playlists.add("shared.webp")
    playlists.add("shared.webp", userid=2)
    playlists.add("kept.webp")
    playlists.files(
        "deleted.webp", "thumb_deleted.webp", "shared.webp", "thumb_shared.webp",
        "kept.webp", "thumb_kept.webp",
    )

    response = client.delete(f"/playlists/{deleted}/delete")
    assert response.status_code == 200
    assert playlists.table.get_by_id(deleted) is None
    assert playlists.names() == {"shared.webp", "thumb_shared.webp", "kept.webp", "thumb_kept.webp"}

    assert client.delete(f"/playlists/{shared}/delete").status_code == 200
    assert playlists.names() == {"shared.webp", "thumb_shared.webp", "kept.webp", "thumb_kept.webp"}


def test_replace_image_api_keeps_new_cover_and_cleans_old_pair(playlists, client):
    playlistid = playlists.add("old.webp")
    playlists.add("kept.webp")
    playlists.files("old.webp", "thumb_old.webp", "kept.webp", "thumb_kept.webp")
    upload = io.BytesIO()
    Image.new("RGB", (16, 8), "blue").save(upload, format="PNG")
    upload.seek(0)

    response = client.put(f"/playlists/{playlistid}/update", data={
        "name": "Updated", "settings": json.dumps({"pinned": False}),
        "image": (upload, "synthetic.png", "image/png"),
    })

    assert response.status_code == 200, response.get_json()
    image = playlists.table.get_by_id(playlistid).image
    assert image != "old.webp"
    assert playlists.names() == {image, "thumb_" + image, "kept.webp", "thumb_kept.webp"}
    with Image.open(playlists.directory / image) as original:
        assert original.size == (16, 8)
    with Image.open(playlists.directory / ("thumb_" + image)) as thumb:
        assert thumb.size == (500, 250)
