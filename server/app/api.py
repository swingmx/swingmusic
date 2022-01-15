import os
import urllib
from flask import Blueprint, request
from app import functions, instances, helpers, cache

bp = Blueprint('api', __name__, url_prefix='')

all_the_f_music = []
home_dir = helpers.home_dir


all_the_f_music = helpers.getAllSongs()

def initialize() -> None:
    helpers.create_config_dir()
    helpers.check_for_new_songs()

initialize()

@bp.route('/')
def adutsfsd():
    return "^ _ ^"


@bp.route('/search')
def search_by_title():
    if not request.args.get('q'):
        query = "mexican girl"
    else:
        query = request.args.get('q')

    albums = []
    artists = []

    s = instances.songs_instance.find_song_by_title(query)
    al = instances.songs_instance.search_songs_by_album(query)
    ar = instances.songs_instance.search_songs_by_artist(query)

    for song in al:
        album_obj = {
            "name": song["album"],
            "artists": song["artists"],
        }

        if album_obj not in albums:
            albums.append(album_obj)

    for album in albums:
        # try:
        #     image = convert_one_to_json(instances.songs_instance.get_song_by_album(album['name'], album['artists']))['image']
        # except:
        #     image: None

        album['image'] = "image"

    for song in ar:

        for artist in song["artists"]:
            if query.lower() in artist.lower():

                artist_obj = {
                    "name": artist,
                }

                if artist_obj not in artists:
                    artists.append(artist_obj)

    return {'songs': helpers.remove_duplicates(s), 'albums': albums, 'artists': artists}


@bp.route('/populate')
def x():
    functions.populate()
    return "🎸"


@bp.route("/album/<album>/<artist>/artists")
@cache.cached()
def get_album_artists(album, artist):
    album = album.replace('|', '/')
    artist = artist.replace('|', '/')
    
    tracks = []

    for track in all_the_f_music:
        if track["album"] == album and track["album_artist"] == artist:
            tracks.append(track)

    artists = []

    for track in tracks:
        print(track['artists'])

        for artist in track['artists']:
            if artist not in artists:
                artists.append(artist)

    final_artists = []
    for artist in artists:
        artist_obj = {
            "name": artist,
            "image": "http://127.0.0.1:8900/images/artists/" + artist.replace('/', '::') + ".jpg"
        }
        final_artists.append(artist_obj)

    return {'artists': final_artists}


@bp.route("/populate/images")
def populate_images():
    functions.populate_images()
    return "Done"


@bp.route("/artist/<artist>")
@cache.cached()
def getArtistData(artist: str):
    print(artist)
    artist = urllib.parse.unquote(artist)
    artist_obj = instances.artist_instance.get_artists_by_name(artist)

    def getArtistSongs():
        songs = instances.songs_instance.find_songs_by_artist(artist)

        return songs

    artist_songs = getArtistSongs()
    songs = helpers.remove_duplicates(artist_songs)

    def getArtistAlbums():
        artist_albums = []
        albums_with_count = []

        albums = instances.songs_instance.find_songs_by_album_artist(artist)

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

    if folder == "home":
        req_dir = home_dir

    dir_content = os.scandir(os.path.join(home_dir, req_dir))

    folders = []

    for entry in dir_content:
        if entry.is_dir() and not entry.name.startswith('.'):
            files_in_dir = helpers.run_fast_scandir(
                entry.path, [".flac", ".mp3"])[1]

            if len(files_in_dir) != 0:
                dir = {
                    "name": entry.name,
                    "count": len(files_in_dir),
                    "path": entry.path.replace(home_dir, "")
                }

                folders.append(dir)

        # if entry.is_file():
        #     if isValidFile(entry.name) == True:
        #         file = instances.songs_instance.find_song_by_path(entry.path)

        #         if not file:
        #             getTags(entry.path)

    # songs_array = instances.songs_instance.find_songs_by_folder(
    #     req_dir)

    songs = []

    for x in all_the_f_music:
        if x['folder'] == req_dir:
            songs.append(x)

    return {"files": helpers.remove_duplicates(songs), "folders": sorted(folders, key=lambda i: i['name'])}

@bp.route('/qwerty')
def populateArtists():
    all_songs = instances.songs_instance.get_all_songs()

    artists = []

    for song in all_songs:
        for a in song['artists']:
            a_obj = {
                "name": a,
            }

            if a_obj not in artists:
                artists.append(a_obj)

            instances.artist_instance.insert_artist(a_obj)

    return {'songs': artists}

@bp.route('/albums')
def getAlbums():
    s = instances.songs_instance.get_all_songs()

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
@cache.cached()
def getAlbumSongs(query: str):
    album = query.split('::')[0].replace('|', '/')
    artist = query.split('::')[1].replace('|', '/')

    songs = []

    for track in all_the_f_music:
        if track['album'] == album and track['album_artist'] == artist:
            songs.append(track)

    album_obj = {
        "name": album,
        "count": len(songs),
        "duration": sum(song['length'] for song in songs),
        "image": songs[0]['image'],
        "artist": songs[0]['album_artist']
    }

    return {'songs': helpers.remove_duplicates(songs), 'info': album_obj}
