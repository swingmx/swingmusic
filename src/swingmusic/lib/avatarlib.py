"""
This library contains all the functions related to user images.
"""

import logging
import secrets
from typing import BinaryIO

from PIL import Image, ImageOps

from swingmusic.settings import Paths

logger = logging.getLogger(__name__)

AVATAR_SIZE = 250
MAX_AVATAR_BYTES = 5 * 1024 * 1024


def crop_avatar(img: Image.Image) -> Image.Image:
    """
    Returns a 250x250 crop from the center of `img`, upright per its EXIF orientation.
    """
    img = ImageOps.exif_transpose(img)

    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA" if "transparency" in img.info or "A" in img.mode else "RGB")

    return ImageOps.fit(img, (AVATAR_SIZE, AVATAR_SIZE), Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def save_avatar(file: BinaryIO, userid: int) -> str:
    """
    Saves a cropped webp of `file` and returns its filename.

    Raises `PIL.UnidentifiedImageError` if `file` is not an image.
    """
    with Image.open(file) as img:
        avatar = crop_avatar(img)

    filename = f"{userid}{secrets.token_hex(3)}.webp"
    avatar.save(Paths().user_img_path / filename, "webp")
    return filename


def delete_avatar(filename: str | None) -> None:
    """
    Deletes a saved user image.
    """
    if not filename:
        return

    try:
        (Paths().user_img_path / filename).unlink(missing_ok=True)
    except OSError as e:
        logger.exception("could not delete user image", exc_info=e)
