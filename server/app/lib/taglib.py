import os
from io import BytesIO

import mutagen
from app import settings
from mutagen.flac import FLAC, MutagenError
from mutagen.id3 import ID3
from PIL import Image


def parse_album_art(filepath: str):
    """
    Returns the album art for a given audio file.
    """

    if filepath.endswith(".flac"):
        try:
            audio = FLAC(filepath)
            return audio.pictures[0].data
        except:
            return None
    elif filepath.endswith(".mp3"):
        try:
            audio = ID3(filepath)
            return audio.getall("APIC")[0].data
        except:
            return None


def extract_thumb(filepath: str, webp_path: str) -> bool:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """
    img_path = os.path.join(settings.THUMBS_PATH, webp_path)
    tsize = settings.THUMB_SIZE

    if os.path.exists(img_path):
        img_size = os.path.getsize(filepath)

        if img_size > 0:
            return True

    album_art = parse_album_art(filepath)

    if album_art is not None:
        img = Image.open(BytesIO(album_art))

        try:
            small_img = img.resize((tsize, tsize), Image.ANTIALIAS)
            small_img.save(img_path, format="webp")
        except OSError:
            try:
                png = img.convert("RGB")
                small_img = png.resize((tsize, tsize), Image.ANTIALIAS)
                small_img.save(webp_path, format="webp")
            except:
                return False

        return True
    else:
        return False


def parse_artist_tag(tags):
    """
    Parses the artist tag from an audio file.
    """
    try:
        artists = tags["artist"][0]
    except (KeyError, IndexError):
        artists = "Unknown"

    return artists


def parse_title_tag(tags, full_path: str):
    """
    Parses the title tag from an audio file.
    """
    try:
        title = tags["title"][0]
    except (KeyError, IndexError):
        title = full_path.split("/")[-1]

    return title


def parse_album_artist_tag(tags):
    """
    Parses the album artist tag from an audio file.
    """
    try:
        albumartist = tags["albumartist"][0]
    except (KeyError, IndexError):
        albumartist = "Unknown"

    return albumartist


def parse_album_tag(tags, full_path: str):
    """
    Parses the album tag from an audio file.
    """
    try:
        album = tags["album"][0]
    except (KeyError, IndexError):
        album = full_path.split("/")[-1]

    return album


def parse_genre_tag(tags):
    """
    Parses the genre tag from an audio file.
    """
    try:
        genre = tags["genre"][0]
    except (KeyError, IndexError):
        genre = "Unknown"

    return genre


def parse_date_tag(tags):
    """
    Parses the date tag from an audio file.
    """
    try:
        date = tags["date"][0]
    except (KeyError, IndexError):
        date = "Unknown"

    return date


def parse_track_number(tags):
    """
    Parses the track number from an audio file.
    """
    try:
        track_number = int(tags["tracknumber"][0])
    except (KeyError, IndexError, ValueError):
        track_number = 1

    return track_number


def parse_disc_number(tags):
    """
    Parses the disc number from an audio file.
    """
    try:
        disc_number = int(tags["discnumber"][0])
    except (KeyError, IndexError, ValueError):
        disc_number = 1

    return disc_number


def parse_copyright(tags):
    try:
        copyright = str(tags["copyright"][0])
    except (KeyError, IndexError, ValueError):
        copyright = None

    return copyright


def get_tags(fullpath: str) -> dict | None:
    """
    Returns a dictionary of tags for a given file.
    """
    try:
        tags = mutagen.File(fullpath, easy=True)
    except MutagenError:
        return None

    tags = {
        "artists": parse_artist_tag(tags),
        "title": parse_title_tag(tags, fullpath),
        "albumartist": parse_album_artist_tag(tags),
        "album": parse_album_tag(tags, fullpath),
        "genre": parse_genre_tag(tags),
        "date": parse_date_tag(tags)[:4],
        "tracknumber": parse_track_number(tags),
        "discnumber": parse_disc_number(tags),
        "copyright": parse_copyright(tags),
        "length": round(tags.info.length),
        "bitrate": round(int(tags.info.bitrate) / 1000),
        "filepath": fullpath,
        "folder": os.path.dirname(fullpath),
    }

    return tags
