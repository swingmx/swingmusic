"""
Filesystem cover art discovery, ranking, and thumbnail refresh.
"""

from io import BytesIO
import re
from pathlib import Path

from PIL import Image, UnidentifiedImageError

from swingmusic.settings import Defaults

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# name token -> score. Positive tokens mark front covers,
# negative tokens mark scans, booklets and other non-cover art.
TOKEN_SCORES = {
    "front": 8,
    "cover": 7,
    "folder": 6,
    "album": 5,
    "box": 2,
    "cd": -3,
    "small": -4,
    "back": -6,
    "spine": -6,
    "inlay": -6,
    "inside": -6,
    "disc": -8,
    "tray": -8,
    "booklet": -8,
    "matrix": -8,
}


def list_candidate_images(folder: Path) -> list[Path]:
    """
    Returns image files in the folder and its immediate subfolders.
    Hidden files and folders are skipped.
    """
    images: list[Path] = []

    try:
        entries = sorted(folder.iterdir())
    except OSError:
        return images

    subfolders: list[Path] = []

    for entry in entries:
        if entry.name.startswith("."):
            continue

        if entry.is_dir():
            subfolders.append(entry)
        elif entry.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(entry)

    for subfolder in subfolders:
        try:
            children = sorted(subfolder.iterdir())
        except OSError:
            continue

        for child in children:
            if child.name.startswith("."):
                continue

            if child.is_file() and child.suffix.lower() in IMAGE_EXTENSIONS:
                images.append(child)

    return images


def get_name_score(filename: str) -> int:
    """
    Scores a filename by summing the scores of known tokens in it.
    Trailing digits are stripped from tokens before matching (eg. "cd1" -> "cd").
    """
    tokens = re.split(r"[^a-z0-9]+", filename.lower())
    score = 0

    for token in tokens:
        token = token.rstrip("0123456789")
        score += TOKEN_SCORES.get(token, 0)

    return score


def get_dimension_score(filepath: Path) -> int:
    """
    Scores an image by aspect ratio and resolution.
    Near-square, reasonably sized images score highest.
    """
    try:
        with Image.open(filepath) as img:
            width, height = img.size
    except (OSError, ValueError):
        return -4

    if width == 0 or height == 0:
        return -4

    ratio = max(width, height) / min(width, height)

    if ratio <= 1.1:
        score = 5
    elif ratio <= 1.4:
        score = 2
    elif ratio <= 1.8:
        score = -2
    else:
        score = -8

    short_edge = min(width, height)

    if short_edge >= 500:
        score += 4
    elif short_edge >= 256:
        score += 2
    else:
        score -= 4

    return score


def score_cover_image(filepath: Path, folder: Path) -> int:
    """
    Scores an image as an album cover candidate.
    Images directly in the album folder rank above ones in subfolders.
    """
    score = get_name_score(filepath.stem)
    score += get_dimension_score(filepath)

    if filepath.parent == folder:
        score += 2

    return score


def rank_cover_images(folder: Path) -> list[Path]:
    """
    Returns candidate cover images in the folder, best first.
    """
    images = list_candidate_images(folder)
    return sorted(
        images,
        key=lambda i: score_cover_image(i, folder),
        reverse=True,
    )


def find_best_cover(folder: Path) -> Path | None:
    """
    Returns the best cover image in the folder, or None.
    """
    ranked = rank_cover_images(folder)
    return ranked[0] if ranked else None


SOURCE_EMBEDDED = "embedded"


def _thumb_filename(albumhash: str) -> str:
    return albumhash + ".webp"


def _source_sidecar(albumhash: str, paths) -> Path:
    return paths.og_thumb_path / (albumhash + ".src")


def _thumb_targets(albumhash: str, paths) -> list[tuple[Path, int]]:
    filename = _thumb_filename(albumhash)
    return [
        (paths.lg_thumb_path / filename, Defaults.LG_THUMB_SIZE),
        (paths.sm_thumb_path / filename, Defaults.SM_THUMB_SIZE),
        (paths.xsm_thumb_path / filename, Defaults.XSM_THUMB_SIZE),
        (paths.md_thumb_path / filename, Defaults.MD_THUMB_SIZE),
        (paths.og_thumb_path / filename, Defaults.OG_THUMB_SIZE),
    ]


def save_album_image(img: Image.Image, albumhash: str, paths) -> bool:
    """
    Writes webp thumbs at all sizes. Returns True on success.
    """
    width, height = img.size
    if width == 0 or height == 0:
        return False

    ratio = width / height

    try:
        for path, size in _thumb_targets(albumhash, paths):
            path.parent.mkdir(parents=True, exist_ok=True)
            if width <= size:
                img.save(path, "webp")
            else:
                img.resize((size, int(size / ratio)), Image.LANCZOS).save(path, "webp")
    except OSError:
        if img.mode != "RGB":
            try:
                return save_album_image(img.convert("RGB"), albumhash, paths)
            except OSError:
                return False
        return False

    return True


def write_thumb_source(albumhash: str, paths, source: Path | None) -> None:
    sidecar = _source_sidecar(albumhash, paths)
    sidecar.parent.mkdir(parents=True, exist_ok=True)
    sidecar.write_text(
        source.as_posix() if source is not None else SOURCE_EMBEDDED,
        encoding="utf-8",
    )


def read_thumb_source(albumhash: str, paths) -> str | None:
    sidecar = _source_sidecar(albumhash, paths)
    if not sidecar.exists():
        return None

    text = sidecar.read_text(encoding="utf-8").strip()
    return text or None


def delete_album_thumbs(albumhash: str, paths) -> None:
    """
    Removes cached thumbs and the source sidecar for an album.
    """
    for path, _ in _thumb_targets(albumhash, paths):
        path.unlink(missing_ok=True)

    _source_sidecar(albumhash, paths).unlink(missing_ok=True)


def _og_thumb_path(albumhash: str, paths) -> Path:
    return paths.og_thumb_path / _thumb_filename(albumhash)


def album_art_needs_refresh(
    albumhash: str,
    folder: Path,
    paths,
    overwrite: bool = False,
) -> bool:
    """
    True if cached thumbs are missing, stale, or should be rebuilt.
    """
    if overwrite:
        return True

    og_path = _og_thumb_path(albumhash, paths)
    cover = find_best_cover(folder)
    recorded = read_thumb_source(albumhash, paths)

    if not og_path.exists() or og_path.stat().st_size == 0:
        return True

    if cover is not None:
        if recorded is None or recorded == SOURCE_EMBEDDED:
            return True

        if Path(recorded) != cover:
            return True

        try:
            if cover.stat().st_mtime > og_path.stat().st_mtime:
                return True
        except OSError:
            return True

    if recorded is not None and recorded != SOURCE_EMBEDDED:
        if not Path(recorded).exists():
            return True

    return False


def _save_from_path(image_path: Path, albumhash: str, paths) -> bool:
    try:
        with Image.open(image_path) as img:
            img.load()
            if save_album_image(img, albumhash, paths):
                write_thumb_source(albumhash, paths, image_path)
                return True
    except (OSError, UnidentifiedImageError, ValueError):
        return False

    return False


def _save_from_embedded(audio_files: list[str], albumhash: str, paths) -> bool:
    from swingmusic.lib.taglib import parse_album_art

    for filepath in audio_files:
        try:
            album_art = parse_album_art(filepath)
        except (FileNotFoundError, OSError):
            continue

        if album_art is None:
            continue

        try:
            img = Image.open(BytesIO(album_art))
        except (UnidentifiedImageError, OSError):
            continue

        try:
            if save_album_image(img, albumhash, paths):
                write_thumb_source(albumhash, paths, None)
                return True
        finally:
            img.close()

    return False


def refresh_album_art(
    albumhash: str,
    folder: Path,
    audio_files: list[str],
    paths,
    overwrite: bool = False,
) -> bool:
    """
    Refresh cached album thumbs from the folder cover, then embedded art.

    Returns True if thumbs exist after the call. If no source remains,
    deletes cached thumbs and returns False.
    """
    if not overwrite and not album_art_needs_refresh(albumhash, folder, paths):
        og_path = _og_thumb_path(albumhash, paths)
        return og_path.exists() and og_path.stat().st_size > 0

    cover = find_best_cover(folder)
    if cover is not None and _save_from_path(cover, albumhash, paths):
        return True

    if _save_from_embedded(audio_files, albumhash, paths):
        return True

    delete_album_thumbs(albumhash, paths)
    return False


def is_library_image(path: str | Path) -> bool:
    return Path(path).suffix.lower() in IMAGE_EXTENSIONS


def library_watch_patterns() -> list[str]:
    from swingmusic.utils.filesystem import SUPPORTED_FILES

    patterns = [f"*{ext}" for ext in SUPPORTED_FILES]
    patterns.extend(f"*{ext}" for ext in sorted(IMAGE_EXTENSIONS))
    return patterns


def _album_folders_for_image(image_path: Path) -> list[Path]:
    parent = image_path.parent
    folders = [parent]
    if parent.parent != parent:
        folders.append(parent.parent)
    return folders


def refresh_art_for_image(
    image_path: str | Path,
    paths=None,
    tracks_in_path=None,
) -> None:
    """
    Rebuild thumbs for albums that could own this cover image.

    `image_path` may already be deleted; the parent/grandparent folders
    are still used to find matching tracks.
    """
    if paths is None:
        from swingmusic.settings import Paths

        paths = Paths()

    if tracks_in_path is None:
        from swingmusic.store.tracks import TrackStore

        tracks_in_path = TrackStore.get_tracks_in_path

    image_path = Path(image_path)
    seen: set[str] = set()

    for folder in _album_folders_for_image(image_path):
        folder_posix = folder.as_posix()
        tracks = [
            track
            for track in tracks_in_path(folder_posix)
            if Path(track.folder).as_posix() == folder_posix
        ]
        if not tracks:
            continue

        by_album: dict[str, list] = {}
        for track in tracks:
            by_album.setdefault(track.albumhash, []).append(track)

        for albumhash, album_tracks in by_album.items():
            if albumhash in seen:
                continue

            seen.add(albumhash)
            refresh_album_art(
                albumhash,
                Path(album_tracks[0].folder),
                [track.filepath for track in album_tracks],
                paths,
                overwrite=True,
            )
