"""
Uploaded artist images.
"""

import time
from typing import BinaryIO

from PIL import Image, ImageOps

from swingmusic.db.userdata import LibDataTable
from swingmusic.lib.colorlib import get_blurhash, get_image_colors
from swingmusic.settings import Defaults, Paths
from swingmusic.store.artists import ArtistMapEntry

IMAGE_SIZE = 512
MAX_IMAGE_BYTES = 15 * 1024 * 1024


def crop_square(img: Image.Image) -> Image.Image:
    """
    Returns a centered IMAGE_SIZE square of `img`, upright per its EXIF orientation.
    """
    img = ImageOps.exif_transpose(img)

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info or "A" in img.mode else "RGB")

    return ImageOps.fit(img, (IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def image_files(artisthash: str):
    """
    Returns the (path, size) of each saved size of an artist image.
    """
    paths = Paths()
    name = f"{artisthash}.webp"

    return [
        (paths.lg_artist_img_path / name, IMAGE_SIZE),
        (paths.md_artist_img_path / name, Defaults.MD_ARTIST_IMG_SIZE),
        (paths.sm_artist_img_path / name, Defaults.SM_ARTIST_IMG_SIZE),
    ]


def save_libdata(artisthash: str, color: str, extra: dict):
    """
    Writes the artist's color and merges `extra` into its library data.
    """
    existing = LibDataTable.find_one(artisthash, type="artist")
    merged = {**((existing or {}).get("extra") or {}), **extra}

    if existing is None:
        LibDataTable.insert_one(
            {"itemhash": "artist" + artisthash, "itemtype": "artist", "color": color, "extra": merged}
        )
    else:
        LibDataTable.update_one("artist" + artisthash, {"color": color, "extra": merged})


def refresh_colors(entry: ArtistMapEntry, version: int):
    """
    Recomputes the artist's color and blurhash from its small image and saves them with `version`.
    """
    small = image_files(entry.artist.artisthash)[-1][0]
    color, blurhash = "", ""

    if small.exists():
        color = next(iter(get_image_colors(small)), "")
        blurhash = get_blurhash(small) or ""

    save_libdata(
        entry.artist.artisthash,
        color,
        {"blurhash": blurhash, "image_version": version},
    )
    entry.update_color_info(color, blurhash)
    entry.artist.set_image_version(version)


def save_artist_image(file: BinaryIO, entry: ArtistMapEntry):
    """
    Saves `file` as the artist's image in every size and updates its colors.

    Raises `PIL.UnidentifiedImageError` if `file` is not an image.
    """
    with Image.open(file) as img:
        square = crop_square(img)

    for path, size in image_files(entry.artist.artisthash):
        path.parent.mkdir(parents=True, exist_ok=True)
        image = square if size == IMAGE_SIZE else square.resize((size, size), Image.Resampling.LANCZOS)
        image.save(path, "webp")

    refresh_colors(entry, int(time.time()))

