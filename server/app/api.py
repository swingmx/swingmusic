import os
from re import sub
import requests
import urllib
import time


from progress.bar import Bar
from mutagen.flac import MutagenError
from flask import Blueprint, request, send_from_directory

from app.models import AllSongs, Folders, Artists
from app.configs import default_configs

from app.helpers import (
    all_songs_instance,
    convert_one_to_json,
    getTags,
    convert_to_json,
    remove_duplicates,
    save_image,
    isValidFile,
    create_config_dir,
    extract_thumb,
    home_dir, app_dir,
    run_fast_scandir
)

bp = Blueprint('api', __name__, url_prefix='')

artist_instance = Artists()
folder_instance = Folders()


def main_whatever():
    create_config_dir()


main_whatever()


@bp.route('/search')
def search_by_title():
    if not request.args.get('q'):
        query = "mexican girl"
    else:
        query = request.args.get('q')

    all_songs = []

    songs = all_songs_instance.find_song_by_title(query)
    all_songs.append(convert_to_json(songs))

    songs_by_albums = all_songs_instance.find_songs_by_album(query)
    all_songs.append(convert_to_json(songs_by_albums))

    songs_by_artists = all_songs_instance.find_songs_by_artist(query)
    all_songs.append(convert_to_json(songs_by_artists))

    return {'songs': all_songs}


@bp.route('/populate')
def populate():
    '''
    Populate the database with all songs in the music directory

    checks if the song is in the database, if not, it adds it
    also checks if the album art exists in the image path, if not tries to
    extract it.
    '''
    files = run_fast_scandir(home_dir, [".flac", ".mp3"])[1]

    bar = Bar('Processing', max=len(files))

    for file in files:
        file_in_db_obj = all_songs_instance.find_song_by_path(file)
        song_obj = convert_one_to_json(file_in_db_obj)

        try:
            image = song_obj['image']

            if not os.path.exists(os.path.join(app_dir, 'images', 'thumbnails', image)):
                extract_thumb(file)
        except:
            image = None

        if image is None:
            try:
                getTags(file)
            except MutagenError:
                pass

        bar.next()

    bar.finish()
    return {'msg': 'updated everything'}


@bp.route('/file/<file_id>')
def send_audio(file_id):
    song_obj = all_songs_instance.get_song_by_id(file_id)
    loaded_song = convert_one_to_json(song_obj)

    filepath = loaded_song['filepath'].split('/')[-1]
    print(loaded_song['folder'] + filepath)

    return send_from_directory(home_dir + loaded_song['folder'], filepath)


@bp.route("/folder/artists")
def get_folder_artists():
    dir = request.args.get('dir')

    songs = all_songs_instance.find_songs_by_folder(dir)
    songs_array = convert_to_json(songs)
    without_duplicates = remove_duplicates(songs_array)

    artists = []

    for song in without_duplicates:
        this_artists = song['artists'].split(', ')

        for artist in this_artists:

            if artist not in artists:
                artists.append(artist)

    final_artists = []

    for artist in artists[:15]:
        artist_obj = artist_instance.find_artists_by_name(artist)

        if artist_obj != []:
            final_artists.append(convert_to_json(artist_obj))

    return {'artists': final_artists}


@bp.route("/populate/images")
def populate_images():
    all_songs = all_songs_instance.get_all_songs()
    songs_array = convert_to_json(all_songs)
    remove_duplicates(songs_array)

    artists = []

    for song in songs_array:
        this_artists = song['artists'].split(', ')

        for artist in this_artists:
            if artist not in artists:
                artists.append(artist)

    bar = Bar('Processing images', max=len(artists))
    for artist in artists:
        file_path = app_dir + '/images/artists/' + artist + '.jpg'

        if not os.path.exists(file_path):
            url = 'https://api.deezer.com/search/artist?q={}'.format(artist)
            response = requests.get(url)
            data = response.json()

            try:
                image_path = data['data'][0]['picture_xl']
            except:
                image_path = None

            if image_path is not None:
                try:
                    save_image(image_path, file_path)
                    artist_obj = {
                        'name': artist
                    }

                    artist_instance.insert_artist(artist_obj)
                except:
                    pass
        else:
            pass

        bar.next()

    bar.finish()

    artists_in_db = artist_instance.get_all_artists()
    artists_in_db_array = convert_to_json(artists_in_db)

    return {'sample': artists_in_db_array[:25]}


@bp.route("/artist")
def getArtistData():
    artist = urllib.parse.unquote(request.args.get('q'))
    artist_obj = artist_instance.find_artists_by_name(artist)
    artist_obj_json = convert_to_json(artist_obj)

    def getArtistSongs():
        songs = all_songs_instance.find_songs_by_artist(artist)
        songs_array = convert_to_json(songs)

        return songs_array

    artist_songs = getArtistSongs()
    songs = remove_duplicates(artist_songs)

    def getArtistAlbums():
        artist_albums = []
        albums_with_count = []

        albums = all_songs_instance.find_songs_by_album_artist(artist)
        albums_array = convert_to_json(albums)

        for song in songs:
            song['artists'] = song['artists'].split(', ')

        for song in albums_array:
            if song['album'] not in artist_albums:
                artist_albums.append(song['album'])

        for album in artist_albums:
            count = 0
            length = 0

            for song in artist_songs:
                if song['album'] == album:
                    count = count + 1
                    length = length + song['length']

            album_ = {
                "title": album,
                "count": count,
                "length": length
            }

            albums_with_count.append(album_)

        return albums_with_count

    return {'artist': artist_obj_json, 'songs': songs, 'albums': getArtistAlbums()}


@bp.route("/")
def getFolderTree():
    start = time.time()

    req_dir = request.args.get('f')
    last_id = request.args.get('last_id')

    if req_dir is not None:
        requested_dir = os.path.join(home_dir, req_dir)
        print(requested_dir)
    else:
        requested_dir = home_dir

    dir_content = os.scandir(requested_dir)

    folders = []
    files = []

    for entry in dir_content:
        if entry.is_dir() and not entry.name.startswith('.'):
            files_in_dir = run_fast_scandir(entry.path, [".flac", ".mp3"])[1]

            if len(files_in_dir) != 0:
                dir = {
                    "name": entry.name,
                    "count": len(files_in_dir),
                    "path": entry.path.replace(home_dir, "")
                }

                folders.append(dir)

        if entry.is_file():
            if isValidFile(entry.name) == True:
                songs_array = all_songs_instance.find_songs_by_folder(
                    req_dir, last_id)
                songs = convert_to_json(songs_array)
                for song in songs:
                    song['artists'] = song['artists'].split(', ')

                files = songs

    for file in files:
        file['filepath'] = file['filepath'].replace(home_dir, '')

    dir_content.close()
    end = time.time()
    print(end - start)
    return {"requested": req_dir, "files": files[:25], "folders": folders}


@bp.route('/image/<img_type>/<image_id>')
def send_image(img_type, image_id):
    if img_type == "thumbnail":
        song_obj = all_songs_instance.get_song_by_id(image_id)
        loaded_song = convert_one_to_json(song_obj)

        img_dir = app_dir + "/images/thumbnails"
        image = loaded_song['image']

    if img_type == "artist":
        artist_obj = artist_instance.get_artist_by_id(image_id)
        artist = convert_one_to_json(artist_obj)

        img_dir = app_dir + "/images/artists"

        image = artist['name'] + ".jpg"
        print(img_dir + image)

    return send_from_directory(img_dir, image)
