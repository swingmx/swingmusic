from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from swingmusic.lib.coverart import (
    IMAGE_EXTENSIONS,
    is_library_image,
    library_watch_patterns,
    refresh_album_art,
    refresh_art_for_image,
)


def _make_paths(tmp_path: Path) -> SimpleNamespace:
    thumbs = tmp_path / "thumbnails"
    paths = SimpleNamespace(
        lg_thumb_path=thumbs / "large",
        sm_thumb_path=thumbs / "small",
        xsm_thumb_path=thumbs / "xsmall",
        md_thumb_path=thumbs / "medium",
        og_thumb_path=thumbs / "original",
    )
    for folder in (
        paths.lg_thumb_path,
        paths.sm_thumb_path,
        paths.xsm_thumb_path,
        paths.md_thumb_path,
        paths.og_thumb_path,
    ):
        folder.mkdir(parents=True)
    return paths


class FakeTrack:
    def __init__(self, albumhash: str, folder: str, filepath: str):
        self.albumhash = albumhash
        self.folder = folder
        self.filepath = filepath


def test_watch_patterns_include_audio_and_images():
    patterns = {p.lower() for p in library_watch_patterns()}

    assert "*.mp3" in patterns
    for ext in IMAGE_EXTENSIONS:
        assert f"*{ext}" in patterns


def test_is_library_image_detects_cover_files():
    assert is_library_image("/music/album/cover.jpg") is True
    assert is_library_image("/music/album/folder.PNG") is True
    assert is_library_image("/music/album/song.mp3") is False


def test_refresh_art_for_image_rebuilds_thumbs_for_album_folder(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    Image.new("RGB", (32, 32), (255, 0, 0)).save(cover)

    paths = _make_paths(tmp_path)
    track = FakeTrack("albumhash1", album.as_posix(), str(album / "song.mp3"))

    refresh_art_for_image(
        cover,
        paths=paths,
        tracks_in_path=lambda path: [track] if path == album.as_posix() else [],
    )

    assert (paths.og_thumb_path / "albumhash1.webp").exists()


def test_refresh_art_for_image_handles_cover_in_subfolder(tmp_path: Path):
    album = tmp_path / "album"
    scans = album / "scans"
    scans.mkdir(parents=True)
    cover = scans / "front.png"
    Image.new("RGB", (32, 32), (0, 255, 0)).save(cover)

    paths = _make_paths(tmp_path)
    track = FakeTrack("albumhash1", album.as_posix(), str(album / "song.mp3"))

    refresh_art_for_image(
        cover,
        paths=paths,
        tracks_in_path=lambda path: [track] if path == album.as_posix() else [],
    )

    assert (paths.og_thumb_path / "albumhash1.webp").exists()


def test_refresh_art_for_image_clears_thumbs_when_cover_removed(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    Image.new("RGB", (32, 32), (255, 0, 0)).save(cover)

    paths = _make_paths(tmp_path)
    refresh_album_art("albumhash1", album, [], paths)
    og = paths.og_thumb_path / "albumhash1.webp"
    assert og.exists()

    cover.unlink()
    track = FakeTrack("albumhash1", album.as_posix(), str(album / "song.mp3"))

    refresh_art_for_image(
        cover,
        paths=paths,
        tracks_in_path=lambda path: [track] if path == album.as_posix() else [],
    )

    assert not og.exists()
