"""
This library contains all the functions related to playlists.
"""
import os
import random
import string
from datetime import datetime
from typing import Any

from PIL import Image
from PIL import ImageSequence

from app import settings
from app.logger import log


def create_thumbnail(image: Any, img_path: str) -> str:
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(settings.APP_DIR, "images", "playlists", thumb_path)

    aspect_ratio = image.width / image.height

    new_w = round(250 * aspect_ratio)

    thumb = image.resize((new_w, 250), Image.ANTIALIAS)
    thumb.save(full_thumb_path, "webp")

    return thumb_path


def create_gif_thumbnail(image: Any, img_path: str):
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(settings.APP_DIR, "images", "playlists", thumb_path)

    frames = []

    for frame in ImageSequence.Iterator(image):
        aspect_ratio = frame.width / frame.height

        new_w = round(250 * aspect_ratio)

        thumb = frame.resize((new_w, 250), Image.ANTIALIAS)
        frames.append(thumb)

    frames[0].save(full_thumb_path, save_all=True, append_images=frames[1:])

    return thumb_path


def save_p_image(file, pid: str):
    """
    Saves the image of a playlist to the database.
    """
    img = Image.open(file)

    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    img_path = pid + str(random_str) + ".webp"

    full_img_path = os.path.join(settings.APP_DIR, "images", "playlists", img_path)

    if file.content_type == "image/gif":
        frames = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        frames[0].save(full_img_path, save_all=True, append_images=frames[1:])
        create_gif_thumbnail(img, img_path=img_path)

        return img_path

    img.save(full_img_path, "webp")
    create_thumbnail(img, img_path=img_path)

    return img_path


class ValidatePlaylistThumbs:
    """
    Removes all unused images in the images/playlists folder.
    """

    def __init__(self) -> None:
        images = []
        playlists = Get.get_all_playlists()

        log.info("Validating playlist thumbnails")
        for playlist in playlists:
            if playlist.image:
                img_path = playlist.image.split("/")[-1]
                thumb_path = playlist.thumb.split("/")[-1]

                images.append(img_path)
                images.append(thumb_path)

        p_path = os.path.join(settings.APP_DIR, "images", "playlists")

        for image in os.listdir(p_path):
            if image not in images:
                os.remove(os.path.join(p_path, image))

        log.info("Validating playlist thumbnails ... ✅")


def create_new_date():
    return datetime.now()


# TODO: Fix ValidatePlaylistThumbs
