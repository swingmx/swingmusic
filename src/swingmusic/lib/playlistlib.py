"""
This library contains all the functions related to playlists.
"""
import random
import string
import logging
from PIL import Image, ImageSequence

from swingmusic import settings
from swingmusic.models.track import Track
from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore

logger = logging.getLogger(__name__)

def create_thumbnail(image: Image, img_name: str) -> str:
    """
    Creates a 250 px high thumbnail from the Image.
    It will keep the aspect ratio.

    Images are saved in the playlist-img path

    :param image: Image object.
    :param img_name: Name of image.
    :return: Filename of image.
    """

    aspect_ratio = image.width / image.height
    new_w = round(250 * aspect_ratio)
    thumb = image.resize((new_w, 250), Image.Resampling.LANCZOS)

    thumb_filename = "thumb_" + img_name
    thumb_path = settings.Paths().playlist_img_path / thumb_filename

    thumb.save(thumb_path, "webp")

    return thumb_filename


def create_gif_thumbnail(image: Image, img_name: str):
    """
    Creates a 250 px high thumbnail from the provided GIF.
    Keeps the aspect ratio.

    Images are saved in the playlist-img path

    :param image: Image object.
    :param img_name: Name of image.
    :return: Filename of image.
    """
    thumb_name = "thumb_" + img_name
    thumb_path = settings.Paths().playlist_img_path / thumb_name

    frames = []
    for frame in ImageSequence.Iterator(image):
        aspect_ratio = frame.width / frame.height
        new_w = round(250 * aspect_ratio)
        thumb = frame.resize((new_w, 250), Image.Resampling.LANCZOS)

        frames.append(thumb)

    frames[0].save(thumb_path, save_all=True, append_images=frames[1:])

    return thumb_name


def save_p_image(img: Image, pid: int, content_type: str = None, filename: str = None) -> str:
    """
    Saves a playlist banner image and returns the filepath.
    """
    # img = Image.open(file)

    random_str = "".join(random.choices(string.ascii_letters + string.digits, k=5))

    if not filename:
        filename = str(pid) + str(random_str) + ".webp"

    full_img_path = settings.Paths().playlist_img_path / filename

    if content_type == "image/gif":
        frames = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())

        frames[0].save(full_img_path, save_all=True, append_images=frames[1:])
        create_gif_thumbnail(img, img_path=filename)

        return filename

    img.save(full_img_path, "webp")
    create_thumbnail(img, img_name=filename)

    return filename


def duplicate_images(images: list):
    if len(images) == 1:
        images *= 4
    elif len(images) == 2:
        images += list(reversed(images))
    elif len(images) == 3:
        images = images + images[:1]

    return images

# TODO: mutable var in param.
def get_first_4_images(
        tracks: list[Track] = [],
        trackhashes: list[str] = []
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


def cleanup_playlist_images() -> None:
    """
    Deletes all unlinked files in playlist-img folder.
    All files not present in the PlaylistTable will get deleted
    """
    # Import here to avoid circular import
    from swingmusic.db.userdata import PlaylistTable

    playlists = PlaylistTable.get_all()
    linked_images = {p.image for p in playlists if p.image and p.image != "None"}

    playlist_dir = settings.Paths().playlist_img_path

    # Find unlinked images (including thumbnails)
    for file in playlist_dir.iterdir():
        if not file.isfile:
            continue

        name = file.name # not stem. PlaylistTable saves with extension
        if file not in linked_images:
            if name.removeprefix("thumb_") not in linked_images:
                continue

            try:
                file.unlink(missing_ok=True)
            except OSError as e:
                logger.exception("could not delete file", exc_info=e)
