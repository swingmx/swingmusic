"""
This library contains all the functions related to playlists.
"""

import os
import random
import string
from typing import Any

from PIL import Image, ImageSequence

from swingmusic import settings
from swingmusic.models.track import Track
from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore


def create_thumbnail(image: Any, img_path: str) -> str:
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(
        settings.Paths.get_app_dir(), "images", "playlists", thumb_path
    )

    aspect_ratio = image.width / image.height

    new_w = round(250 * aspect_ratio)

    thumb = image.resize((new_w, 250), Image.Resampling.LANCZOS)
    thumb.save(full_thumb_path, "webp")

    return thumb_path


def create_gif_thumbnail(image: Any, img_path: str):
    """
    Creates a 250 x 250 thumbnail from a playlist image
    """
    thumb_path = "thumb_" + img_path
    full_thumb_path = os.path.join(
        settings.Paths.get_app_dir(), "images", "playlists", thumb_path
    )

    frames = []

    for frame in ImageSequence.Iterator(image):
        aspect_ratio = frame.width / frame.height

        new_w = round(250 * aspect_ratio)

        thumb = frame.resize((new_w, 250), Image.Resampling.LANCZOS)
        frames.append(thumb)

    frames[0].save(full_thumb_path, save_all=True, append_images=frames[1:])

    return thumb_path


def save_p_image(
    img: Image, pid: int, content_type: str = None, filename: str = None
) -> str:
    """
    Saves a playlist banner image and returns the filepath.
    """
    # img = Image.open(file)

    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    if not filename:
        filename = str(pid) + str(random_str) + ".webp"

    full_img_path = os.path.join(settings.Paths.get_playlist_img_path(), filename)

    if content_type == "image/gif":
        frames = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        frames[0].save(full_img_path, save_all=True, append_images=frames[1:])
        create_gif_thumbnail(img, img_path=filename)

        return filename

    img.save(full_img_path, "webp")
    create_thumbnail(img, img_path=filename)

    return filename


def duplicate_images(images: list):
    if len(images) == 1:
        images *= 4
    elif len(images) == 2:
        images += list(reversed(images))
    elif len(images) == 3:
        images = images + images[:1]

    return images


def get_first_4_images(
    tracks: list[Track] = [], trackhashes: list[str] = []
) -> list[dict["str", str]]:
    """
    Returns images of the first 4 albums that appear in the track list.

    When tracks are not passed, trackhashes need to be passed.
    Tracks are then resolved from the store.
    """
    if len(trackhashes) > 0:
        tracks = TrackStore.get_tracks_by_trackhashes(trackhashes)

    albums = []

    for track in tracks:
        if track.albumhash not in albums:
            albums.append(track.albumhash)

            if len(albums) == 4:
                break

    albums = AlbumStore.get_albums_by_hashes(albums)
    images = [
        {
            "image": album.image,
            "color": album.color,
        }
        for album in albums
    ]

    if len(images) == 4:
        return images

    return duplicate_images(images)
