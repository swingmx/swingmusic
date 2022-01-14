"""
This module contains mimi functions for the server.
"""

import os
import threading
import time
import requests

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC

from io import BytesIO
from PIL import Image

from app import instances
from app import functions

home_dir = os.path.expanduser('~') + "/"
app_dir = home_dir + '/.musicx'


def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

@background
def check_for_new_songs():
    flag = False

    while flag is False:
        functions.populate()
        time.sleep(300)


def run_fast_scandir(dir: str, ext: str) -> list:
    """
    Scans a directory for files with a specific extension. Returns a list of files and folders in the directory.
    """

    subfolders = []
    files = []

    for f in os.scandir(dir):
        if f.is_dir() and not f.name.startswith('.'):
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files


def extract_thumb(path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """

    webp_path = path.split('/')[-1] + '.webp'
    img_path = app_dir + "/images/thumbnails/" + webp_path

    if os.path.exists(img_path):
        return webp_path

    if path.endswith('.flac'):
        try:
            audio = FLAC(path)
            album_art = audio.pictures[0].data
        except:
            album_art = None
    elif path.endswith('.mp3'):
        try:
            audio = ID3(path)
            album_art = audio.getall('APIC')[0].data
        except:
            album_art = None

    if album_art is None:
        return "null.webp"
    else:
        img = Image.open(BytesIO(album_art))

        try:
            small_img = img.resize((150, 150), Image.ANTIALIAS)
            small_img.save(img_path, format="webp")
        except OSError:
            try:
                png = img.convert('RGB')
                small_img = png.resize((150, 150), Image.ANTIALIAS)
                small_img.save(img_path, format="webp")
                print('{} :: was png'.format(
                    img_path
                ))

            except:
                img_path = None

    return webp_path


def getTags(full_path: str) -> dict:
    """
    Returns a dictionary of tags for a given file.
    """

    if full_path.endswith('.flac'):
        try:
            audio = FLAC(full_path)
        except:
            return
    elif full_path.endswith('.mp3'):
        try:
            audio = MP3(full_path)
        except:
            return

    try:
        artists = audio['artist'][0]
    except KeyError:
        try:
            artists = audio['TPE1'][0]
        except:
            artists = 'Unknown'
    except IndexError:
        artists = 'Unknown'

    try:
        album_artist = audio['albumartist'][0]
    except KeyError:
        try:
            album_artist = audio['TPE2'][0]
        except:
            album_artist = 'Unknown'
    except IndexError:
        album_artist = 'Unknown'

    try:
        title = audio['title'][0]
    except KeyError:
        try:
            title = audio['TIT2'][0]
        except:
            title = full_path.split('/')[-1]
    except:
        title = full_path.split('/')[-1]

    try:
        album = audio['album'][0]
    except KeyError:
        try:
            album = audio['TALB'][0]
        except:
            album = "Unknown"
    except IndexError:
        album = "Unknown"

    try:
        genre = audio['genre'][0]
    except KeyError:
        try:
            genre = audio['TCON'][0]
        except:
            genre = "Unknown"
    except IndexError:
        genre = "Unknown"

    img_path = extract_thumb(full_path)

    tags = {
        "filepath": full_path.replace(home_dir, ''),
        "folder": os.path.dirname(full_path).replace(home_dir, ""),
        "title": title,
        "artists": artists,
        "album_artist": album_artist,
        "album": album,
        "genre": genre,
        "length": round(audio.info.length),
        "bitrate": audio.info.bitrate,
        "image": img_path,
        "type": {
            "name": None,
            "id": None
        }
    }

    instances.songs_instance.insert_song(tags)
    return tags


def remove_duplicates(array: list) -> list:
    """
    Removes duplicates from a list. Returns a list without duplicates.
    """

    song_num = 0

    while song_num < len(array) - 1:
        for index, song in enumerate(array):
            try:

                if array[song_num]["title"] == song["title"] and array[song_num]["album"] == song["album"] and array[song_num]["artists"] == song["artists"] and index != song_num:
                    array.remove(song)
            except:
                print('whe')
        song_num += 1

    return array


def save_image(url: str, path: str) -> None:
    """
    Saves an image from a url to a path.
    """

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path, 'JPEG')


def isValidFile(filename: str) -> bool:
    """
    Checks if a file is valid. Returns True if it is, False if it isn't.
    """

    if filename.endswith('.flac') or filename.endswith('.mp3'):
        return True
    else:
        return False


def create_config_dir() -> None:
    """
    Creates the config directory if it doesn't exist.
    """

    home_dir = os.path.expanduser('~')
    config_folder = home_dir + app_dir

    dirs = ["", "/images", "/images/artists", "/images/thumbnails"]

    for dir in dirs:
        if not os.path.exists(config_folder + dir):
            os.makedirs(config_folder + dir)


def getAllSongs() -> None:
    """
    Gets all songs under the ~/ directory.
    """
    
    tracks = []
    tracks.extend(instances.songs_instance.get_all_songs())

    for track in tracks:
        try:
            os.chmod(os.path.join(home_dir, track['filepath']), 0o755)
        except FileNotFoundError:
            instances.songs_instance.remove_song_by_filepath(
                os.path.join(home_dir, track['filepath']))
        if track['image'] is not None:
            track['image'] = "http://127.0.0.1:8900/images/thumbnails/" + \
                track['image']

    return tracks
