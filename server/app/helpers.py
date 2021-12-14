from genericpath import exists
import os
import json
import requests
import urllib

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC

from bson import json_util

from io import BytesIO
from PIL import Image

from app.models import AllSongs
from app.configs import default_configs

all_songs_instance = AllSongs()
music_dir = os.environ.get("music_dir")
music_dirs = os.environ.get("music_dirs")

home_dir = os.path.expanduser('~')
app_dir = home_dir + '/.shit'


PORT = os.environ.get("PORT")


def run_fast_scandir(dir, ext):
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


def extract_thumb(path):
    img_path = app_dir + "/images/thumbnails/" + path.split('/')[-1] + '.jpg'

    if os.path.exists(img_path):
        return path.split('/')[-1] + '.jpg'

    if path.endswith('.flac'):
        audio = FLAC(path)
        try:
            album_art = audio.pictures[0].data
        except IndexError:
            album_art = None
    elif path.endswith('.mp3'):
        audio = ID3(path)
        try:
            album_art = audio.getall('APIC')[0].data
        except IndexError:
            album_art = None

    if album_art is not None:

        img = Image.open(BytesIO(album_art))

        try:
            img.save(img_path, 'JPEG')
        except OSError:
            try:
                img.convert('RGB'.save(img_path, 'JPEG'))
            except:
                img_path = None
        return path.split('/')[-1] + '.jpg'


def getTags(full_path):
    if full_path.endswith('.flac'):
        audio = FLAC(full_path)
    elif full_path.endswith('.mp3'):
        audio = MP3(full_path)

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
            title = 'Unknown'
    except IndexError:
        title = 'Unknown'

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
        "filepath": full_path,
        "folder": os.path.dirname(full_path).replace(home_dir, ""),
        "title": title,
        "artists": artists,
        "album_artist": album_artist,
        "album": album,
        "genre": genre,
        "length": round(audio.info.length),
        "bitrate": audio.info.bitrate,
        "image": img_path
    }

    all_songs_instance.insert_song(tags)
    return tags


def convert_one_to_json(song):
    json_song = json.dumps(song, default=json_util.default)
    loaded_song = json.loads(json_song)

    return loaded_song


def convert_to_json(array):
    songs = []

    for song in array:
        json_song = json.dumps(song, default=json_util.default)
        loaded_song = json.loads(json_song)

        songs.append(loaded_song)

    return songs


def get_folders():
    folders = []

    for dir in default_configs['dirs']:
        entry = os.scandir(dir)
        folders.append(entry)


def remove_duplicates(array):
    return array


def save_image(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path, 'JPEG')


def isValidFile(filename):
    if filename.endswith('.flac') or filename.endswith('.mp3'):
        return True
    else:
        return False


def isValidAudioFrom(folder):
    folder_content = os.scandir(folder)
    files = []

    for entry in folder_content:
        if isValidFile(entry.name) == True:
            file = {
                "path": entry.path,
                "name": entry.name
            }

            files.append(file)

    return files


def getFolderContents(filepath, folder):

    folder_name = urllib.parse.unquote(folder)

    path = filepath
    name = filepath.split('/')[-1]
    tags = {}

    if name.endswith('.flac'):
        image_path = folder_name + '/.thumbnails/' + \
            name.replace('.flac', '.jpg')
        audio = FLAC(path)

    if name.endswith('.mp3'):
        image_path = folder_name + '/.thumbnails/' + \
            name.replace('.mp3', '.jpg')
        audio = MP3(path)

    abslt_path = urllib.parse.quote(path.replace(music_dir, ''))

    if os.path.exists(image_path):
        img_url = 'http://localhost:{}/{}'.format(
            PORT,
            urllib.parse.quote(image_path.replace(music_dir, ''))
        )

    try:
        audio_url = 'http://localhost:{}/{}'.format(
            PORT, abslt_path
        )
        tags = getTags(audio_url, audio, img_url, folder_name)
    except:
        pass

    return tags


def create_config_dir():
    home_dir = os.path.expanduser('~')
    config_folder = home_dir + "/.shit"

    dirs = ["", "/images", "/images/artists", "/images/thumbnails"]

    for dir in dirs:
        if not os.path.exists(config_folder + dir):
            os.makedirs(config_folder + dir)
