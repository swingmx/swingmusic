"""
This module contains larger functions for the server
"""

import time
import os
import requests
import random

from mutagen.flac import MutagenError
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.flac import FLAC
from progress.bar import Bar
from PIL import Image
from io import BytesIO

from app import helpers
from app import instances
from app import api


def populate():
    '''
    Populate the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to
    extract it.
    '''
    print('\nchecking for new tracks')
    files = helpers.run_fast_scandir(helpers.home_dir, [".flac", ".mp3"])[1]

    for file in files:
        getTags(file)

    api.all_the_f_music = helpers.getAllSongs()
    print('\ncheck done')


def populate_images():
    all_songs = instances.songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
        this_artists = song['artists'].split(', ')

        for artist in this_artists:
            if artist not in artists:
                artists.append(artist)

    bar = Bar('Processing images', max=len(artists))
    for artist in artists:
        file_path = helpers.app_dir + '/images/artists/' + \
            artist.replace('/', '::') + '.jpg'

        if not os.path.exists(file_path):
            url = 'https://api.deezer.com/search/artist?q={}'.format(artist)

            try:
                response = requests.get(url)
            except requests.ConnectionError:
                print('\n sleeping for 5 seconds')
                time.sleep(5)
                response = requests.get(url)

            data = response.json()

            try:
                img_data = data['data'][0]['picture_xl']
            except:
                img_data = None

            if img_data is not None:
                helpers.save_image(img_data, file_path)

        bar.next()

    bar.finish()


def extract_thumb(path: str) -> str:
    """
    Extracts the thumbnail from an audio file. Returns the path to the thumbnail.
    """

    def use_defaults() -> str:
        """
        Returns a path to a random image in the defaults directory.
        """
        path = "http://127.0.0.1:8900/images/defaults/" + \
            str(random.randint(0, 10)) + '.webp'
        return path

    webp_path = path.split('/')[-1] + '.webp'
    img_path = os.path.join(helpers.app_dir, "images", "thumbnails", webp_path)

    if os.path.exists(img_path):
        return "http://127.0.0.1:8900/images/thumbnails/" + webp_path

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
        return use_defaults()
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
            except:
                return use_defaults()

        final_path = "http://127.0.0.1:8900/images/thumbnails/" + webp_path

        return final_path


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
        "filepath": full_path.replace(helpers.home_dir, ''),
        "folder": os.path.dirname(full_path).replace(helpers.home_dir, ""),
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


def getAlbumBio(title: str, album_artist: str) -> dict:
    last_fm_url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key={}&artist={}&album={}&format=json'.format(
        helpers.last_fm_api_key, album_artist, title)
    
    try:
        response = requests.get(last_fm_url)
        data = response.json()
    except requests.ConnectionError:
        return "None"
    
    try:
        bio = data['album']['wiki']['summary'].split('<a href="https://www.last.fm/')[0]
    except KeyError:
        bio = None

    if bio is None:
        return "None"

    return bio
