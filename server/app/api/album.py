from flask import Blueprint, request
from app import api
from app import helpers, cache
from app import functions
from app.lib import albumslib, trackslib
album_bp = Blueprint("album", __name__, url_prefix="")


@album_bp.route("/")
def say_hi():
    """Returns some text for the default route"""
    return "^ _ ^"


@album_bp.route("/albums")
def get_albums():
    """returns all the albums"""
    albums = []

    for song in api.DB_TRACKS:
        al_obj = {"name": song["album"], "artist": song["artists"]}

        if al_obj not in albums:
            albums.append(al_obj)

    return {"albums": albums}


@album_bp.route("/album/tracks", methods=["POST"])
def get_album_tracks():
    """Returns all the tracks in the given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    songs = trackslib.get_album_tracks(album, artist)
    album = albumslib.find_album(album, artist)

    return {"songs": songs, "info": album}


@album_bp.route("/album/<title>/<artist>/bio")
@cache.cached()
def get_album_bio(title, artist):
    """Returns the album bio for the given album."""
    bio = functions.get_album_bio(title, artist)
    return {"bio": bio}, 200


@album_bp.route("/album/artists", methods=["POST"])
def get_albumartists():
    """Returns a list of artists featured in a given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    tracks = []

    for track in api.TRACKS:
        if track.album == album and track.albumartist == artist:
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
            "image": helpers.check_artist_image(artist),
        }
        final_artists.append(artist_obj)

    return {"artists": final_artists}
