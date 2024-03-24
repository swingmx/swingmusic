from pathlib import Path
from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field
from flask import send_from_directory

from app.settings import Defaults, Paths

bp_tag = Tag(
    name="Images", description="Image filenames are constructured as '{itemhash}.webp'"
)
api = APIBlueprint("imgserver", __name__, url_prefix="/img", abp_tags=[bp_tag])


def send_fallback_img(filename: str = "default.webp"):
    folder = Paths.get_assets_path()
    img = Path(folder) / filename

    if not img.exists():
        return "", 404

    return send_from_directory(folder, filename)


class ImagePath(BaseModel):
    imgpath: str = Field(
        description="The image filename",
        example=Defaults.API_ALBUMHASH + ".webp",
    )


@api.get("/t/o/<imgpath>")
def send_original_thumbnail(path: ImagePath):
    """
    Get original thumbnail
    """
    folder = Paths.get_original_thumb_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img()


@api.get("/t/<imgpath>")
def send_lg_thumbnail(path: ImagePath):
    """
    Get large thumbnail (500 x 500)
    """
    folder = Paths.get_lg_thumb_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img()


@api.get("/t/s/<imgpath>")
def send_sm_thumbnail(path: ImagePath):
    """
    Get small thumbnail (64 x 64)
    """
    folder = Paths.get_sm_thumb_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img()


@api.get("/a/<imgpath>")
def send_lg_artist_image(path: ImagePath):
    """
    Get large artist image (500 x 500)
    """
    folder = Paths.get_artist_img_lg_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img("artist.webp")


@api.get("/a/s/<imgpath>")
def send_sm_artist_image(path: ImagePath):
    """
    Get small artist image (64 x 64)
    """
    folder = Paths.get_artist_img_sm_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img("artist.webp")


class PlaylistImagePath(BaseModel):
    imgpath: str = Field(
        description="The image path",
        example="1.webp",
    )


@api.get("/p/<imgpath>")
def send_playlist_image(path: PlaylistImagePath):
    """
    Get playlist image

    Images are constructed as '{playlist_id}.webp'
    """
    folder = Paths.get_playlist_img_path()
    fpath = Path(folder) / path.imgpath

    if fpath.exists():
        return send_from_directory(folder, path.imgpath)

    return send_fallback_img("playlist.svg")
