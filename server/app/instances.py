"""
All the MongoDB instances are created here.
"""
from app.db.mongodb import albums
from app.db.mongodb import artists
from app.db.mongodb import playlists
from app.db.mongodb import tracks
from app.settings import DB_TYPE

tracks_instance = None
artist_instance = None
album_instance = None
playlist_instance = None

if DB_TYPE == "mongodb":
    tracks_instance = tracks.Tracks()
    artist_instance = artists.Artists()
    album_instance = albums.Albums()
    playlist_instance = playlists.Playlists()
elif DB_TYPE == "sqlite":
    pass
