from dataclasses import dataclass
import os
from io import BytesIO
from pathlib import Path
from pprint import pprint
import re
import sys

import pendulum
from PIL import Image, UnidentifiedImageError
from tinytag import TinyTag

from app.config import UserConfig
from app.settings import Defaults, Paths
from app.utils.hashing import create_hash
from app.utils.parsers import (
    clean_title,
    get_base_title_and_versions,
    parse_feat_from_title,
    remove_prod,
    split_artists,
)
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


def extract_thumb(filepath: str, webp_path: str, overwrite=False) -> bool:
    """
    Extracts the thumbnail from an audio file.
    Returns the path to the thumbnail.
    """
    lg_img_path = os.path.join(Paths.get_lg_thumb_path(), webp_path)
    sm_img_path = os.path.join(Paths.get_sm_thumb_path(), webp_path)
    xms_img_path = os.path.join(Paths.get_xsm_thumb_path(), webp_path)
    md_img_path = os.path.join(Paths.get_md_thumb_path(), webp_path)

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
            img.resize((size, int(size / ratio)), Image.ANTIALIAS).save(path, "webp")

    if not overwrite and os.path.exists(sm_img_path):
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


def parse_date(date_str: str | None) -> int | None:
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

    def __post_init__(self):
        self.artist = split_artists(self.artist)


def extract_artist_title(filename: str):
    path = Path(filename).with_suffix("")

    path = clean_filename(str(path))
    split_result = path.split(" - ")
    split_result = [x.strip() for x in split_result]

    if len(split_result) == 1:
        return ParseData("", split_result[0])

    if len(split_result) > 2:
        try:
            int(split_result[0])

            return ParseData(split_result[1], " - ".join(split_result[2:]))
        except ValueError:
            pass

    artist = split_result[0]
    title = split_result[1]
    return ParseData(artist, title)


def get_tags(filepath: str):
    """
    Returns the tags for a given audio file.
    """

    filetype = filepath.split(".")[-1]
    filename = (filepath.split("/")[-1]).replace(f".{filetype}", "")

    try:
        last_mod = round(os.path.getmtime(filepath))
    except FileNotFoundError:
        return None

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

    parse_data = None

    to_filename = ["title", "album"]
    for tag in to_filename:
        p = getattr(tags, tag)
        if p == "" or p is None:
            parse_data = extract_artist_title(filename)
            title = parse_data.title
            setattr(tags, tag, title)

    parse = ["artist", "albumartist"]
    for tag in parse:
        p = getattr(tags, tag)

        if p == "" or p is None:
            if not parse_data:
                parse_data = extract_artist_title(filename)

            artist = parse_data.artist

            if artist:
                setattr(tags, tag, ", ".join(artist))
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

    # tags.image = f"{tags.albumhash}.webp"
    tags.folder = win_replace_slash(os.path.dirname(filepath))

    tags.date = parse_date(tags.year) or int(last_mod)
    tags.filepath = win_replace_slash(filepath)
    tags.last_mod = last_mod

    tags.artists = tags.artist
    tags.albumartists = tags.albumartist

    split_artist = split_artists(tags.artist)
    split_albumartists = split_artists(tags.albumartist)
    new_title = tags.title

    # TODO: Figure out which is the best spot to create these hashes
    # create albumhash using og_album
    tags.albumhash = create_hash(tags.album or "", tags.albumartist)

    config = UserConfig()

    # extract featured artists
    if config.extractFeaturedArtists:
        feat, new_title = parse_feat_from_title(tags.title)
        original_lower = "-".join([create_hash(a) for a in split_artist])
        split_artist.extend(a for a in feat if create_hash(a) not in original_lower)

    # if no albumartist, assign to the first artist
    if not tags.albumartist:
        tags.albumartist = split_artist[:1]

    # create json objects for artists and albumartists
    tags.artists = [
        {
            "artisthash": create_hash(a, decode=True),
            "name": a,
        }
        for a in split_artist
    ]

    tags.albumartists = [
        {
            "artisthash": create_hash(a, decode=True),
            "name": a,
        }
        for a in split_albumartists
    ]

    tags.artisthashes = list({a["artisthash"] for a in tags.artists + tags.albumartists})


    # remove prod by
    if config.removeProdBy:
        new_title = remove_prod(new_title)

    # if track is a single, ie.
    # if og_title == album, rename album to new_title
    if tags.title == tags.album:
        tags.album = new_title

    # remove remaster from track title
    if config.removeRemasterInfo:
        new_title = clean_title(new_title)

    # save final title
    tags.og_title = tags.title
    tags.title = new_title
    tags.og_album = tags.album

    # clean album title
    if config.cleanAlbumTitle:
        tags.album, _ = get_base_title_and_versions(tags.album, get_versions=False)

    # merge album versions
    if config.mergeAlbums:
        tags.albumhash = create_hash(
            tags.album, *(a["name"] for a in tags.albumartists)
        )

    # process genres
    if tags.genre:
        tags.genre = tags.genre.lower()
        # separators = {"/", ";", "&"}
        separators = set(config.genreSeparators)

        contains_rnb = "r&b" in tags.genre
        contains_rock = "rock & roll" in tags.genre

        if contains_rnb:
            tags.genre = tags.genre.replace("r&b", "RnB")

        if contains_rock:
            tags.genre = tags.genre.replace("rock & roll", "rock")

        for s in separators:
            tags.genre = tags.genre.replace(s, ",")

        tags.genre = tags.genre.split(",")
        tags.genre = [
            {"name": g.strip(), "genrehash": create_hash(g.strip())} for g in tags.genre
        ]

    # sub underscore with space
    tags.title = tags.title.replace("_", " ")
    tags.album = tags.album.replace("_", " ")
    tags.trackhash = create_hash(
        *[a["name"] for a in tags.artists], tags.album, tags.title
    )

    more_extra = {
        "audio_offset": tags.audio_offset,
        "bitdepth": tags.bitdepth,
        "composer": tags.composer,
        "channels": tags.channels,
        "comment": tags.comment,
        "disc_total": tags.disc_total,
        "filesize": tags.filesize,
        "samplerate": tags.samplerate,
        "track_total": tags.track_total,
    }

    tags.extra = {**tags.extra, **more_extra}

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
        "samplerate",
        "track_total",
        "year",
        "bitdepth",
        "artist",
        "albumartist",
    ]

    for tag in to_delete:
        del tags[tag]

    return tags
