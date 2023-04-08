import datetime
import os
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from tinytag import TinyTag

from app.settings import Defaults, Paths
from app.utils.hashing import create_hash
from app.utils.parsers import parse_title_from_filename, parse_artist_from_filename
from app.utils.wintools import win_replace_slash


def parse_album_art(filepath: str):
    """
    Returns the album art for a given audio file.
    """

    try:
        tags = TinyTag.get(filepath, image=True)
        return tags.get_image()
    except:  # pylint: disable=bare-except
        return None


def extract_thumb(filepath: str, webp_path: str) -> bool:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """
    img_path = os.path.join(Paths.LG_THUMBS_PATH, webp_path)
    sm_img_path = os.path.join(Paths.SM_THUMB_PATH, webp_path)

    tsize = Defaults.THUMB_SIZE
    sm_tsize = Defaults.SM_THUMB_SIZE

    def save_image(img: Image.Image):
        img.resize((sm_tsize, sm_tsize), Image.ANTIALIAS).save(sm_img_path, "webp")
        img.resize((tsize, tsize), Image.ANTIALIAS).save(img_path, "webp")

    if os.path.exists(img_path):
        img_size = os.path.getsize(img_path)

        if img_size > 0:
            return True

    album_art = parse_album_art(filepath)

    if album_art is not None:
        try:
            img = Image.open(BytesIO(album_art))
        except (UnidentifiedImageError, OSError):
            return False

        try:
            save_image(img)
        except OSError:
            try:
                png = img.convert("RGB")
                save_image(png)
            except:  # pylint: disable=bare-except
                return False

        return True
    return False


def extract_date(date_str: str | None, filepath: str) -> int:
    try:
        return int(date_str.split("-")[0])
    except:  # pylint: disable=bare-except
        # TODO: USE FILEPATH LAST-MOD DATE instead of current date
        return datetime.date.today().today().year


def get_tags(filepath: str):
    filetype = filepath.split(".")[-1]
    filename = (filepath.split("/")[-1]).replace(f".{filetype}", "")

    try:
        tags = TinyTag.get(filepath)
    except:  # noqa: E722
        return None

    no_albumartist: bool = (tags.albumartist == "") or (tags.albumartist is None)
    no_artist: bool = (tags.artist == "") or (tags.artist is None)

    if no_albumartist and not no_artist:
        tags.albumartist = tags.artist

    if no_artist and not no_albumartist:
        tags.artist = tags.albumartist

    to_filename = ["title", "album"]
    for tag in to_filename:
        p = getattr(tags, tag)
        if p == "" or p is None:
            maybe = parse_title_from_filename(filename)
            setattr(tags, tag, maybe)

    parse = ["artist", "albumartist"]
    for tag in parse:
        p = getattr(tags, tag)

        if p == "" or p is None:
            maybe = parse_artist_from_filename(filename)

            if maybe:
                setattr(tags, tag, ", ".join(maybe))
            else:
                setattr(tags, tag, "Unknown")

    # TODO: Move parsing title, album and artist to startup. (Maybe!)

    to_check = ["album", "year", "albumartist"]
    for prop in to_check:
        p = getattr(tags, prop)
        if (p is None) or (p == ""):
            setattr(tags, prop, "Unknown")

    to_round = ["bitrate", "duration"]
    for prop in to_round:
        try:
            setattr(tags, prop, round(getattr(tags, prop)))
        except TypeError:
            setattr(tags, prop, 0)

    to_int = ["track", "disc"]
    for prop in to_int:
        try:
            setattr(tags, prop, int(getattr(tags, prop)))
        except (ValueError, TypeError):
            setattr(tags, prop, 1)

    try:
        tags.copyright = tags.extra["copyright"]
    except KeyError:
        tags.copyright = None

    tags.albumhash = create_hash(tags.album, tags.albumartist)
    tags.trackhash = create_hash(tags.artist, tags.album, tags.title)
    tags.image = f"{tags.albumhash}.webp"
    tags.folder = win_replace_slash(os.path.dirname(filepath))

    tags.date = extract_date(tags.year, filepath)
    tags.filepath = win_replace_slash(filepath)
    tags.filetype = filetype

    tags = tags.__dict__

    # delete all tag properties that start with _ (tinytag internals)
    for tag in list(tags):
        if tag.startswith("_"):
            del tags[tag]

    to_delete = [
        "filesize",
        "audio_offset",
        "channels",
        "comment",
        "composer",
        "disc_total",
        "extra",
        "samplerate",
        "track_total",
        "year",
    ]

    for tag in to_delete:
        del tags[tag]

    return tags
