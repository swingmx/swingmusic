from app.models import Artists

from app.helpers import (
    all_songs_instance,
    getTags,
    remove_duplicates,
    save_image,
    create_config_dir,
    extract_thumb,
    run_fast_scandir,
    convert_one_to_json,
    convert_to_json,
    home_dir, app_dir,
)

from app import cache

import os
import requests
import urllib

from progress.bar import Bar
from mutagen.flac import MutagenError

from flask import Blueprint, request, send_from_directory


bp = Blueprint('api', __name__, url_prefix='')

artist_instance = Artists()
img_path = "http://127.0.0.1:8900/images/thumbnails/"


all_the_f_music = []


def getAllSongs():
    all_the_f_music.clear()
    all_the_f_music.extend(all_songs_instance.get_all_songs())


def main_whatever():
    create_config_dir()
    # populate()
    getAllSongs()


@bp.route('/')
def adutsfsd():
    for song in all_the_f_music:
        print(os.path.join(home_dir, song['filepath']))
        os.chmod(os.path.join(home_dir, song['filepath']), 0o755)

    return "Done"


main_whatever()


@bp.route('/search')
def search_by_title():
    if not request.args.get('q'):
        query = "mexican girl"
    else:
        query = request.args.get('q')

    albums = []
    artists = []

    s = all_songs_instance.find_song_by_title(query)
    al = all_songs_instance.search_songs_by_album(query)
    ar = all_songs_instance.search_songs_by_artist(query)

    for song in al:
        album_obj = {
            "name": song["album"],
            "artists": song["artists"],
        }

        if album_obj not in albums:
            albums.append(album_obj)

    for album in albums:
        # try:
        #     image = convert_one_to_json(all_songs_instance.get_song_by_album(album['name'], album['artists']))['image']
        # except:
        #     image: None

        album['image'] = "image"

    for song in ar:
        a = song["artists"].split(', ')

        for artist in a:
            if query.lower() in artist.lower():

                artist_obj = {
                    "name": artist,
                }

                if artist_obj not in artists:
                    artists.append(artist_obj)

    return {'songs': remove_duplicates(s), 'albums': albums, 'artists': artists}


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

        try:
            image = file_in_db_obj['image']

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


@bp.route("/folder/artists")
def get_folder_artists():
    dir = request.args.get('dir')

    songs = all_songs_instance.find_songs_by_folder(dir)
    without_duplicates = remove_duplicates(songs)

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
            final_artists.append(artist_obj)

    return {'artists': final_artists}


@bp.route("/populate/images")
def populate_images():
    all_songs = all_songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
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

    return {'sample': artists_in_db[:25]}


@bp.route("/artist/<artist>")
@cache.cached()
def getArtistData(artist: str):
    print(artist)
    artist = urllib.parse.unquote(artist)
    artist_obj = artist_instance.get_artists_by_name(artist)

    def getArtistSongs():
        songs = all_songs_instance.find_songs_by_artist(artist)

        return songs

    artist_songs = getArtistSongs()
    songs = remove_duplicates(artist_songs)

    def getArtistAlbums():
        artist_albums = []
        albums_with_count = []

        albums = all_songs_instance.find_songs_by_album_artist(artist)

        for song in songs:
            song['artists'] = song['artists'].split(', ')

        for song in albums:
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

    return {'artist': artist_obj, 'songs': songs, 'albums': getArtistAlbums()}


@bp.route("/f/<folder>")
@cache.cached()
def getFolderTree(folder: str = None):
    req_dir = folder.replace('|', '/')
    print(folder)

    if folder == "home":
        req_dir = home_dir

    dir_content = os.scandir(os.path.join(home_dir, req_dir))

    folders = []

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

        # if entry.is_file():
        #     if isValidFile(entry.name) == True:
        #         file = all_songs_instance.find_song_by_path(entry.path)

        #         if not file:
        #             getTags(entry.path)

    # songs_array = all_songs_instance.find_songs_by_folder(
    #     req_dir)

    songs = []

    for x in all_the_f_music:
        if x['folder'] == req_dir:
            songs.append(x)

    for song in songs:
        try:
            song['artists'] = song['artists'].split(', ') or None
        except:
            pass

        print(song['image'])
        song['image'] = img_path + song['image']

    return {"files": remove_duplicates(songs), "folders": sorted(folders, key=lambda i: i['name'])}


@bp.route('/qwerty')
def populateArtists():
    all_songs = all_songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
        artist = song['artists'].split(', ')

        for a in artist:
            a_obj = {
                "name": a,
            }

            if a_obj not in artists:
                artists.append(a_obj)

            artist_instance.insert_artist(a_obj)

    return {'songs': artists}


@bp.route('/albums')
def getAlbums():
    s = all_songs_instance.get_all_songs()

    albums = []

    for song in s:
        al_obj = {
            "name": song['album'],
            "artist": song['artists']
        }

        if al_obj not in albums:
            albums.append(al_obj)

    return {'albums': albums}


@bp.route('/albums/<query>')
def getAlbumSongs(query: str):
    album = query.split('::')[0].replace('|', '/')
    artist = query.split('::')[1].replace('|', '/')

    songs = all_songs_instance.find_songs_by_album(album, artist)

    print(artist)

    for song in songs:
        song['artists'] = song['artists'].split(', ')
        song['image'] = img_path + song['image']

    album_obj = {
        "name": album,
        "count": len(songs),
        "duration": sum(song['length'] for song in songs),
        "image": songs[0]['image'],
        "artist": songs[0]['album_artist']
    }
    return {'songs': songs, 'info': album_obj}
