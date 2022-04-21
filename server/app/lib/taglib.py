import os
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.flac import MutagenError
import mutagen
import urllib
from PIL import Image
from io import BytesIO

from app import settings


def return_album_art(filepath: str):
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


def extract_thumb(audio_file_path: str, webp_path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """
    img_path = os.path.join(settings.THUMBS_PATH, webp_path)

    if os.path.exists(img_path):
        return urllib.parse.quote(webp_path)

    album_art = return_album_art(audio_file_path)

    if album_art is not None:
        img = Image.open(BytesIO(album_art))

        try:
            small_img = img.resize((250, 250), Image.ANTIALIAS)
            small_img.save(img_path, format="webp")
        except OSError:
            try:
                png = img.convert("RGB")
                small_img = png.resize((250, 250), Image.ANTIALIAS)
                small_img.save(webp_path, format="webp")
            except:
                return None

        return urllib.parse.quote(webp_path)
    else:
        return None


def parse_artist_tag(audio):
    """
    Parses the artist tag from an audio file.
    """
    try:
        artists = audio["artist"][0]
    except (KeyError, IndexError):
        artists = "Unknown"

    return artists


def parse_title_tag(audio, full_path: str):
    """
    Parses the title tag from an audio file.
    """
    try:
        title = audio["title"][0]
    except (KeyError, IndexError):
        title = full_path.split("/")[-1]

    return title


def parse_album_artist_tag(audio):
    """
    Parses the album artist tag from an audio file.
    """
    try:
        albumartist = audio["albumartist"][0]
    except (KeyError, IndexError):
        albumartist = "Unknown"

    return albumartist


def parse_album_tag(audio, full_path: str):
    """
    Parses the album tag from an audio file.
    """
    try:
        album = audio["album"][0]
    except (KeyError, IndexError):
        album = full_path.split("/")[-1]

    return album


def parse_genre_tag(audio):
    """
    Parses the genre tag from an audio file.
    """
    try:
        genre = audio["genre"][0]
    except (KeyError, IndexError):
        genre = "Unknown"

    return genre


def parse_date_tag(audio):
    """
    Parses the date tag from an audio file.
    """
    try:
        date = audio["date"][0]
    except (KeyError, IndexError):
        date = "Unknown"

    return date


def parse_track_number(audio):
    """
    Parses the track number from an audio file.
    """
    try:
        track_number = audio["tracknumber"][0]
    except (KeyError, IndexError):
        track_number = "Unknown"

    return track_number


def parse_disk_number(audio):
    """
    Parses the disk number from an audio file.
    """
    try:
        disk_number = audio["discnumber"][0]
    except (KeyError, IndexError):
        disk_number = "Unknown"

    return disk_number


def get_tags(fullpath: str) -> dict:
    """
    Returns a dictionary of tags for a given file.
    """
    try:
        audio = mutagen.File(fullpath, easy=True)
    except MutagenError:
        return None

    tags = {
        "artists": parse_artist_tag(audio),
        "title": parse_title_tag(audio, fullpath),
        "albumartist": parse_album_artist_tag(audio),
        "album": parse_album_tag(audio, fullpath),
        "genre": parse_genre_tag(audio),
        "date": parse_date_tag(audio)[:4],
        "tracknumber": parse_track_number(audio),
        "discnumber": parse_disk_number(audio),
        "length": round(audio.info.length),
        "bitrate": round(int(audio.info.bitrate) / 1000),
        "filepath": fullpath,
        "folder": os.path.dirname(fullpath),
    }

    return tags
