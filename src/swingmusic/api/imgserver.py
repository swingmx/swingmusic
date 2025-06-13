from fileinput import filename
from pathlib import Path
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from flask import send_from_directory

from swingmusic.settings import Defaults, Paths
from swingmusic.store.albums import AlbumStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.threading import background
from PIL import Image

bp_tag = Tag(
    name="Images", description="Image filenames are constructured as '{itemhash}.webp'"
)
api = APIBlueprint("imgserver", __name__, url_prefix="/img", abp_tags=[bp_tag])


@background
def cache_thumbnails(filepath: Path, trackhash: str):
    """
    Resizes the image and stores it in the cache directory.
    """
    image = Image.open(filepath)
    path = Path(Paths.get_image_cache_path())
    aspect_ratio = image.width / image.height

    sizes = {
        "xsmall": 64,
        "small": 96,
        "medium": 256,
        "large": 512,
    }

    for size, width in sizes.items():
        width = min(width, image.width)
        height = int(width / aspect_ratio)

        resized_path = path / size / (trackhash + ".webp")
        resized_path.parent.mkdir(parents=True, exist_ok=True)
        image.resize((width, height)).save(resized_path, format="webp")


def find_thumbnail(albumhash: str, pathhash: str):
    # entry = TrackStore.trackhashmap.get(albumhash)
    entry = AlbumStore.albummap.get(albumhash)

    if entry is None:
        return None, None, ""

    track_file = None

    tracks = TrackStore.get_tracks_by_trackhashes(entry.trackhashes)
    for track in tracks:
        if track.pathhash == pathhash:
            track_file = track
            break

    if track_file is None:
        return None, None, ""

    folder = Path(track_file.folder)

    # INFO: Check if the folder has image files
    extensions = [".jpg", ".jpeg", ".png", ".webp"]
    hierarchy = ["cover", "front", "back", "folder", "album", "artwork"]

    images: list[Path] = []
    for item in folder.iterdir():
        if item.suffix in extensions:
            images.append(item)

    if len(images) == 0:
        return None, None, ""

    # INFO: Check if the folder has image files in the hierarchy
    for item in hierarchy:
        for image in images:
            if image.name.lower().startswith(item.lower()):
                return image.parent, image.name, track_file.albumhash

    # INFO: If no image falls in the hierarchy, return the first image
    first_image = images[0]
    return first_image.parent, first_image.name, track_file.albumhash


def send_fallback_img(filename: str = "default.webp"):
    """
    Returns the fallback image from the assets folder.
    """
    folder = Paths.get_assets_path()
    img = Path(folder) / filename

    if not img.exists():
        return "", 404

    return send_from_directory(folder, filename)


def send_file_or_fallback(
    folder: str, filename: str, fallback: str = "default.webp", pathhash: str = ""
):
    """
    Returns the file from the folder or the fallback image.
    """
    fpath = Path(folder) / filename

    if fpath.exists():
        return send_from_directory(folder, filename)

    if pathhash != "":
        # INFO: Check if the image is in the cache
        cache_path = Path(Paths.get_image_cache_path()) / fpath.parent.name / filename
        if cache_path.exists():
            return send_from_directory(cache_path.parent, cache_path.name)

        # INFO: Find the thumbnail
        parent, file, albumhash = find_thumbnail(
            filename.replace(".webp", ""), pathhash
        )

        # INFO: Cache  and send the thumbnail
        if file is not None and parent is not None:
            cache_thumbnails(parent / file, albumhash)
            return send_from_directory(parent, file)

    return send_fallback_img(fallback)


class ImagePath(BaseModel):
    imgpath: str = Field(
        description="The image filename",
        example=Defaults.API_ALBUMHASH + ".webp",
    )


class ImageQuery(BaseModel):
    pathhash: str = Field(
        description="The path hash used to find the thumbnail",
        default="",
    )


# @api.get("/t/o/<imgpath>")
# def send_original_thumbnail(path: ImagePath):
#     """
#     Get original thumbnail
#     """
#     folder = Paths.get_original_thumb_path()
#     fpath = Path(folder) / path.imgpath

#     if fpath.exists():
#         return send_from_directory(folder, path.imgpath)

#     return send_fallback_img()


# TRACK THUMBNAILS
@api.get("/thumbnail/<imgpath>")
def send_lg_thumbnail(path: ImagePath, query: ImageQuery):
    """
    Get large thumbnail (500 x 500)
    """
    folder = Paths.get_lg_thumb_path()
    return send_file_or_fallback(folder, path.imgpath, pathhash=query.pathhash)


@api.get("/thumbnail/xsmall/<imgpath>")
def send_xsm_thumbnail(path: ImagePath, query: ImageQuery):
    """
    Get extra small thumbnail (64px)
    """
    folder = Paths.get_xsm_thumb_path()
    return send_file_or_fallback(folder, path.imgpath, pathhash=query.pathhash)


@api.get("/thumbnail/small/<imgpath>")
def send_sm_thumbnail(path: ImagePath, query: ImageQuery):
    """
    Get small thumbnail (96px)
    """
    folder = Paths.get_sm_thumb_path()
    return send_file_or_fallback(folder, path.imgpath, pathhash=query.pathhash)


@api.get("/thumbnail/medium/<imgpath>")
def send_md_thumbnail(path: ImagePath, query: ImageQuery):
    """
    Get medium thumbnail (256px)
    """
    folder = Paths.get_md_thumb_path()
    return send_file_or_fallback(folder, path.imgpath, pathhash=query.pathhash)


# ARTISTS
@api.get("/artist/<imgpath>")
def send_lg_artist_image(path: ImagePath):
    """
    Get large artist image (500 x 500)
    """
    folder = Paths.get_lg_artist_img_path()
    return send_file_or_fallback(folder, path.imgpath, "artist.webp")


@api.get("/artist/small/<imgpath>")
def send_sm_artist_image(path: ImagePath):
    """
    Get small artist image (128)
    """
    folder = Paths.get_sm_artist_img_path()
    return send_file_or_fallback(folder, path.imgpath, "artist.webp")


@api.get("/artist/medium/<imgpath>")
def send_md_artist_image(path: ImagePath):
    """
    Get medium artist image (256px)
    """
    folder = Paths.get_md_artist_img_path()
    return send_file_or_fallback(folder, path.imgpath, "artist.webp")


# PLAYLISTS
class PlaylistImagePath(BaseModel):
    imgpath: str = Field(
        description="The image path",
        example="1.webp",
    )


@api.get("/playlist/<imgpath>")
def send_playlist_image(path: PlaylistImagePath):
    """
    Get playlist image

    Images are constructed as '{playlist_id}.webp'
    """
    folder = Paths.get_playlist_img_path()
    return send_file_or_fallback(folder, path.imgpath, "playlist.svg")


# MIXES
@api.get("/mix/medium/<imgpath>")
def send_md_mix_image(path: ImagePath):
    """
    Get medium mix image
    """
    folder = Paths.get_md_mixes_img_path()
    return send_file_or_fallback(folder, path.imgpath, "playlist.svg")


@api.get("/mix/small/<imgpath>")
def send_sm_mix_image(path: ImagePath):
    """
    Get small mix image
    """
    folder = Paths.get_sm_mixes_img_path()
    return send_file_or_fallback(folder, path.imgpath, "playlist.svg")
