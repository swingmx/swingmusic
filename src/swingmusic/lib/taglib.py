import pathlib
from dataclasses import dataclass
import os
from io import BytesIO
from pathlib import Path
import re
from typing import Any

import pendulum
from PIL import Image, UnidentifiedImageError
from tinytag import TinyTag

from swingmusic.config import UserConfig
from swingmusic.settings import Defaults, Paths
from swingmusic.utils.hashing import create_hash
from swingmusic.utils.parsers import split_artists


def parse_album_art(filepath: str):
    """
    Returns the album art for a given audio file.

    :params filepath: Path to file
    :returns: `Pil.Image` if available else None
    """
    tags = TinyTag.get(filepath, image=True)
    image = tags.images.any

    if image:
        return image.data

    return None


def extract_thumb(filepath: str, webp_path: str, overwrite=False, paths:Paths=None) -> bool:
    """
    Extracts the thumbnail from an audio file.
    Returns the path to the thumbnail.
    """
    # this function will be run multithreaded.
    # Modules are not cached in concurrent runs.
    # If Paths is tried to be imported
    if paths is None:
        paths = Paths()

    lg_img_path = paths.lg_thumb_path / webp_path
    sm_img_path = paths.sm_thumb_path / webp_path
    xms_img_path = paths.xsm_thumb_path / webp_path
    md_img_path = paths.md_thumb_path / webp_path

    images = [
        (lg_img_path, Defaults.LG_THUMB_SIZE),
        (sm_img_path, Defaults.SM_THUMB_SIZE),
        (xms_img_path, Defaults.XSM_THUMB_SIZE),
        (md_img_path, Defaults.MD_THUMB_SIZE),
    ]

    def save_image(img: Image.Image):
        width, height = img.size
        ratio = width / height

        for path, size in images:
            img.resize((size, int(size / ratio)), Image.LANCZOS).save(path, "webp")

        del img

    if not overwrite and sm_img_path.exists():
        img_size = os.path.getsize(sm_img_path)

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


def parse_date(date_str: str) -> int | None:
    """
    Extracts the date from a string and returns a timestamp.
    """
    try:
        date = pendulum.parse(date_str, strict=False)
        return int(date.timestamp())
    except Exception as e:
        return None


def clean_filename(filename: str):
    if "official" in filename.lower():
        return re.sub(r"\s*\([^)]*official[^)]*\)", "", filename, flags=re.IGNORECASE)

    return filename


@dataclass
class ParseData:
    artist: str
    title: str
    config: UserConfig

    def __post_init__(self):
        self.artist = split_artists(self.artist, self.config)


def extract_artist_title(filename: str, config: UserConfig):
    """
    extract data from filename with specified separators

    :params filename: filename
    :params config: UserConfig for user separators
    """

    path = Path(filename).with_suffix("")

    path = clean_filename(str(path))
    split_result = path.split(" - ")
    split_result = [x.strip() for x in split_result]

    if len(split_result) == 1:
        return ParseData(
            "",
            split_result[0],
            config,
        )

    if len(split_result) > 2:
        try:
            int(split_result[0])

            return ParseData(
                split_result[1],
                " - ".join(split_result[2:]),
                config,
            )
        except ValueError:
            pass

    artist = split_result[0]
    title = split_result[1]
    return ParseData(artist, title, config)


def get_tags(filepath: str, config: UserConfig) -> dict:
    """
    Parse tags from an audio file.
    If tag entries are missing, try getting them from the file name

    :param filepath: Path to file.
    :param config: UserConfig for ``split`` and ``splitignore`` config
    :return: Metadata dict
    :raise FileNotFoundError: If filepath is invalid
    """

    filepath = pathlib.Path(filepath)
    filename = filepath.stem

    if not filepath.exists():
        raise FileNotFoundError(filepath)

    last_mod = round(filepath.stat().st_mtime)
    tags = TinyTag.get(filepath)

    if hasattr(tags, "other"):
        other = tags.other
    else:
        other = {}

    date = parse_date(tags.year or "")
    if date is None:
        date = int(last_mod)

    metadata: dict[str, Any] = {
        "album": tags.album,
        "albumartists": tags.albumartist,
        "artists": tags.artist,
        "title": tags.title,
        "last_mod": last_mod,
        "filepath": filepath.as_posix(),
        "folder": filepath.parent.as_posix(),
        "bitrate": tags.bitrate,
        "duration": tags.duration,
        "track": tags.track,
        "disc": tags.disc,
        "genres": tags.genre,
        "copyright": " ".join(other.get("copyright", [])), # INFO: Extract copyright from extra data
        "extra": {},
        "date": date
    }


    # check the necessary tags and set them
    no_albumartist: bool = (tags.albumartist == "") or (tags.albumartist is None)
    no_artist: bool = (tags.artist == "") or (tags.artist is None)

    if no_albumartist and not no_artist:
        # INFO: If no albumartist, use the artist
        metadata["albumartists"] = tags.artist

    if no_artist and not no_albumartist:
        # INFO: If no artist, use the albumartist
        metadata["artists"] = tags.albumartist

    parse_data = None

    # INFO: If title or album is empty, extract the album and title from the filename
    to_filename = ["title", "album"]
    for tag in to_filename:
        p = metadata[tag]
        if p == "" or p is None:
            parse_data = extract_artist_title(filename, config)
            title = parse_data.title.replace("_", " ")
            metadata[tag] = title

    # INFO: If artist or albumartist is empty
    # extract the artist and albumartist from the filename
    parse = ["artists", "albumartists"]
    for tag in parse:
        p = metadata[tag]

        if p == "" or p is None:
            if not parse_data:
                parse_data = extract_artist_title(filename, config)

            artist = parse_data.artist

            if artist:
                metadata[tag] = ", ".join(artist)
            else:
                metadata[tag] = "Unknown"


    # make values beautiful
    # INFO: If these are empty, set to "Unknown"
    to_check = ["album", "albumartists"]
    for prop in to_check:
        if not metadata[prop]:
            metadata[prop] = "Unknown"

    # INFO: Round the bitrate and duration
    to_round = ["bitrate", "duration"]
    for prop in to_round:
        try:
            metadata[prop] = int(getattr(tags, prop))
        except TypeError:
            metadata[prop] = 0

    # INFO: Convert these to int
    to_int = ["track", "disc"]
    for prop in to_int:
        try:
            metadata[prop] = int(getattr(tags, prop))
        except (ValueError, TypeError):
            metadata[prop] = 1


    # generate hash
    # create albumhash using og_album
    metadata["albumhash"] = create_hash(
        tags.album or "", metadata.get("albumartists", "")
    )

    metadata["trackhash"] = create_hash(
        metadata.get("artists", ""),
        metadata.get("album", ""),
        metadata.get("title", ""),
    )



    # extract extra information not already in tags
    extra: dict[str, Any] = {
        k: v for k, v in tags.as_dict().items() if not k in metadata
    }

    extra["hashinfo"] = {
        "algo": "sha1",
        "format": "[:5]+[-5:]",  # first 5 + last 5 chars
    }


    # REMOVE EMPTY VALUES
    to_pop = ["filename", "artists", "albumartist", "year"]
    for key, value in extra.items():
        # None --bool--> False --not--> True
        # []   --bool--> False --not--> True
        # ""   --bool--> False --not--> True
        # [""] --bool--> True  --not--> False

        if isinstance(value, list) and not "".join(value):
            to_pop.append(key)
            continue

        if not value:
            to_pop.append(key)

    for key in to_pop:
        extra.pop(key, None)


    metadata["extra"] = extra
    return metadata
