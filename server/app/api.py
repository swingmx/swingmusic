import os
import urllib
from flask import Blueprint, request
from app import functions, instances, helpers, cache

bp = Blueprint('api', __name__, url_prefix='')

home_dir = helpers.home_dir

all_the_f_music = helpers.getAllSongs()


def initialize() -> None:
    """
    Runs all the necessary setup functions.
    """
    helpers.create_config_dir()
    # helpers.check_for_new_songs()


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
    tracks = []

    albums_dicts = []
    artists_dicts = []

    for track in all_the_f_music:
        if query.lower() in track.title.lower():
            tracks.append(track)

        if query.lower() in track.album.lower():
            albums.append(track)

        if query.lower() in str(track.artists).lower():
            artists.append(track)

    for song in albums:
        album_obj = {
            "name": song.album,
            "artist": song.album_artist,
        }

        if album_obj not in albums_dicts:
            albums_dicts.append(album_obj)

    for album in albums_dicts:
        for track in albums:
            if album['name'] == track.album:
                album['image'] = track.image

    for song in artists:
        for artist in song.artists:
            if query.lower() in artist.lower():

                artist_obj = {
                    "name": artist,
                    "image": "http://0.0.0.0:8900/images/artists/" + artist.replace("/", "::") + ".webp"
                }

                if artist_obj not in artists_dicts:
                    artists_dicts.append(artist_obj)

    tracks = helpers.remove_duplicates(tracks)

    if len(tracks) > 5:
        more_tracks = True
    else:
        more_tracks = False

    if len(artists_dicts) > 8:
        more_artists = True
    else:
        more_artists = False

    if len(albums_dicts) > 8:
        more_albums = True
    else:
        more_albums = False

    return {'data': [
        {'tracks': tracks[:5], 'more': more_tracks},
        {'albums': albums_dicts[:8], 'more': more_albums},
        {'artists': artists_dicts[:8], 'more': more_artists}
    ]}


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
        if track.album == album and track.album_artist == artist:
            tracks.append(track)

    artists = []

    for track in tracks:
        for artist in track.artists:
            if artist not in artists:
                artists.append(artist)

    final_artists = []
    for artist in artists:
        artist_obj = {
            "name": artist,
            "image": "http://0.0.0.0:8900/images/artists/" + artist.replace('/', '::') + ".webp"
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
def getFolderTree(folder: str):
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
                    "path": entry.path.replace(home_dir, ""),
                }

                folders.append(dir)

    songs = []

    for track in all_the_f_music:
        if track.folder == req_dir:
            songs.append(track)

    return {"files": helpers.remove_duplicates(songs), "folders": sorted(folders, key=lambda i: i['name'])}



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
        if track.album == album and track.album_artist == artist:
            songs.append(track)

    songs = helpers.remove_duplicates(songs)

    album_obj = {
        "name": album,
        "count": len(songs),
        "duration": "56 Minutes",
        "image": songs[0].image,
        "artist": songs[0].album_artist,
        "artist_image": "http://127.0.0.1:8900/images/artists/" + songs[0].album_artist.replace('/', '::') + ".webp"
    }

    return {'songs': songs, 'info': album_obj}


@bp.route('/album/<title>/<artist>/bio')
@cache.cached()
def drop_db(title, artist):
    bio = functions.getAlbumBio(title, artist)
    return {'bio': bio}, 200

