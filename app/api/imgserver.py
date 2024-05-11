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
    """
    Returns the fallback image from the assets folder.
    """
    folder = Paths.get_assets_path()
    img = Path(folder) / filename

    if not img.exists():
        return "", 404

    return send_from_directory(folder, filename)


def send_file_or_fallback(folder: str, filename: str, fallback: str = "default.webp"):
    """
    Returns the file from the folder or the fallback image.
    """
    fpath = Path(folder) / filename

    if fpath.exists():
        return send_from_directory(folder, filename)

    return send_fallback_img(fallback)


class ImagePath(BaseModel):
    imgpath: str = Field(
        description="The image filename",
        example=Defaults.API_ALBUMHASH + ".webp",
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
def send_lg_thumbnail(path: ImagePath):
    """
    Get large thumbnail (500 x 500)
    """
    folder = Paths.get_lg_thumb_path()
    return send_file_or_fallback(folder, path.imgpath)


@api.get("/thumbnail/xsmall/<imgpath>")
def send_xsm_thumbnail(path: ImagePath):
    """
    Get extra small thumbnail (64px)
    """
    folder = Paths.get_xsm_thumb_path()
    return send_file_or_fallback(folder, path.imgpath)


@api.get("/thumbnail/small/<imgpath>")
def send_sm_thumbnail(path: ImagePath):
    """
    Get small thumbnail (96px)
    """
    folder = Paths.get_sm_thumb_path()
    return send_file_or_fallback(folder, path.imgpath)


@api.get("/thumbnail/medium/<imgpath>")
def send_md_thumbnail(path: ImagePath):
    """
    Get medium thumbnail (256px)
    """
    folder = Paths.get_md_thumb_path()
    return send_file_or_fallback(folder, path.imgpath)


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
