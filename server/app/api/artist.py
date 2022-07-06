"""
Contains all the artist(s) routes.
"""
import urllib

from app import cache
from app import helpers
from app import instances
from flask import Blueprint

artist_bp = Blueprint("artist", __name__, url_prefix="/")

# @artist_bp.route("/artist/<artist>")
# @cache.cached()
# def get_artist_data(artist: str):
#     """Returns the artist's data, tracks and albums"""
#     artist = urllib.parse.unquote(artist)
#     artist_obj = instances.artist_instance.get_artists_by_name(artist)

#     def get_artist_tracks():
#         songs = instances.tracks_instance.find_songs_by_artist(artist)

#         return songs

#     artist_songs = get_artist_tracks()
#     songs = helpers.remove_duplicates(artist_songs)

#     def get_artist_albums():
#         artist_albums = []
#         albums_with_count = []

#         albums = instances.tracks_instance.find_songs_by_albumartist(artist)

#         for song in albums:
#             if song["album"] not in artist_albums:
#                 artist_albums.append(song["album"])

#         for album in artist_albums:
#             count = 0
#             length = 0

#             for song in artist_songs:
#                 if song["album"] == album:
#                     count = count + 1
#                     length = length + song["length"]

#             album_ = {"title": album, "count": count, "length": length}

#             albums_with_count.append(album_)

#         return albums_with_count

#     return {
#         "artist": artist_obj,
#         "songs": songs,
#         "albums": get_artist_albums()
#     }
