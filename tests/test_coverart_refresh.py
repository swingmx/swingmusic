import io
import os
import time
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from swingmusic.lib.coverart import album_art_needs_refresh, refresh_album_art
from swingmusic.lib.taglib import extract_thumb


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


def _write_image(path: Path, color: tuple[int, int, int], size: int = 32) -> None:
    Image.new("RGB", (size, size), color).save(path)


def _thumb_color(path: Path) -> tuple[int, int, int]:
    with Image.open(path) as img:
        return img.convert("RGB").getpixel((0, 0))


def _is_mostly(color: tuple[int, int, int], expected: tuple[int, int, int], slack: int = 25) -> bool:
    return all(abs(channel - target) <= slack for channel, target in zip(color, expected))


def test_refresh_album_art_writes_thumbs_from_folder_cover(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    _write_image(album / "cover.png", (255, 0, 0))

    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"

    assert refresh_album_art(albumhash, album, [], paths) is True

    og = paths.og_thumb_path / f"{albumhash}.webp"
    assert og.exists()
    assert _is_mostly(_thumb_color(og), (255, 0, 0))


def test_refresh_replaces_thumbs_when_folder_cover_changes(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    _write_image(cover, (255, 0, 0))

    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"

    refresh_album_art(albumhash, album, [], paths)
    og = paths.og_thumb_path / f"{albumhash}.webp"
    assert _is_mostly(_thumb_color(og), (255, 0, 0))

    _write_image(cover, (0, 0, 255))
    later = time.time() + 10
    os.utime(cover, (later, later))

    assert album_art_needs_refresh(albumhash, album, paths) is True
    assert refresh_album_art(albumhash, album, [], paths) is True
    assert _is_mostly(_thumb_color(og), (0, 0, 255))


def test_refresh_deletes_thumbs_when_cover_removed_and_no_embedded(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    _write_image(cover, (255, 0, 0))

    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"

    refresh_album_art(albumhash, album, [], paths)
    og = paths.og_thumb_path / f"{albumhash}.webp"
    assert og.exists()

    cover.unlink()

    assert album_art_needs_refresh(albumhash, album, paths) is True
    assert refresh_album_art(albumhash, album, [], paths) is False
    assert not og.exists()
    assert not (paths.sm_thumb_path / f"{albumhash}.webp").exists()


def test_refresh_prefers_folder_cover_over_embedded(tmp_path: Path, monkeypatch):
    album = tmp_path / "album"
    album.mkdir()
    _write_image(album / "cover.png", (255, 0, 0))

    blue = io.BytesIO()
    Image.new("RGB", (16, 16), (0, 0, 255)).save(blue, "PNG")
    monkeypatch.setattr(
        "swingmusic.lib.taglib.parse_album_art",
        lambda filepath: blue.getvalue(),
    )

    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"
    audio = str(album / "track.mp3")

    assert refresh_album_art(albumhash, album, [audio], paths) is True
    og = paths.og_thumb_path / f"{albumhash}.webp"
    assert _is_mostly(_thumb_color(og), (255, 0, 0))


def test_refresh_falls_back_to_embedded_when_folder_cover_removed(
    tmp_path: Path, monkeypatch
):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    _write_image(cover, (255, 0, 0))

    blue = io.BytesIO()
    Image.new("RGB", (16, 16), (0, 0, 255)).save(blue, "PNG")
    monkeypatch.setattr(
        "swingmusic.lib.taglib.parse_album_art",
        lambda filepath: blue.getvalue(),
    )

    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"
    audio = str(album / "track.mp3")

    refresh_album_art(albumhash, album, [audio], paths)
    cover.unlink()

    assert refresh_album_art(albumhash, album, [audio], paths) is True
    og = paths.og_thumb_path / f"{albumhash}.webp"
    assert _is_mostly(_thumb_color(og), (0, 0, 255))


def test_extract_thumb_uses_embedded_art_when_no_folder_cover(
    tmp_path: Path, monkeypatch
):
    album = tmp_path / "album"
    album.mkdir()
    audio = album / "song.mp3"
    audio.write_bytes(b"not a real mp3")

    red = io.BytesIO()
    Image.new("RGB", (16, 16), (255, 0, 0)).save(red, "PNG")
    monkeypatch.setattr(
        "swingmusic.lib.taglib.parse_album_art",
        lambda filepath: red.getvalue(),
    )

    paths = _make_paths(tmp_path)
    assert extract_thumb(str(audio), "albumhash1.webp", paths=paths) is True
    og = paths.og_thumb_path / "albumhash1.webp"
    assert og.exists()
    assert _is_mostly(_thumb_color(og), (255, 0, 0))


def test_extract_thumb_uses_folder_cover(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    _write_image(album / "cover.png", (255, 0, 0))
    audio = album / "song.mp3"
    audio.write_bytes(b"not a real mp3")

    paths = _make_paths(tmp_path)
    assert extract_thumb(str(audio), "albumhash1.webp", paths=paths) is True
    og = paths.og_thumb_path / "albumhash1.webp"
    assert og.exists()
    assert _is_mostly(_thumb_color(og), (255, 0, 0))


def test_extract_thumb_refreshes_when_folder_cover_changes(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    cover = album / "cover.png"
    _write_image(cover, (255, 0, 0))
    audio = album / "song.mp3"
    audio.write_bytes(b"not a real mp3")

    paths = _make_paths(tmp_path)
    extract_thumb(str(audio), "albumhash1.webp", paths=paths)

    _write_image(cover, (0, 0, 255))
    later = time.time() + 10
    os.utime(cover, (later, later))

    extract_thumb(str(audio), "albumhash1.webp", overwrite=False, paths=paths)
    og = paths.og_thumb_path / "albumhash1.webp"
    assert _is_mostly(_thumb_color(og), (0, 0, 255))


def test_album_art_needs_refresh_when_overwrite_requested(tmp_path: Path):
    album = tmp_path / "album"
    album.mkdir()
    _write_image(album / "cover.png", (255, 0, 0))
    paths = _make_paths(tmp_path)
    albumhash = "albumhash1"

    refresh_album_art(albumhash, album, [], paths)
    assert album_art_needs_refresh(albumhash, album, paths) is False
    assert album_art_needs_refresh(albumhash, album, paths, overwrite=True) is True
