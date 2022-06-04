"""
All the MongoDB instances are created here.
"""
from app.db.mongodb import albums
from app.db.mongodb import artists
from app.db.mongodb import playlists
from app.db.mongodb import tracks

tracks_instance = tracks.Tracks()
artist_instance = artists.Artists()
album_instance = albums.Albums()
playlist_instance = playlists.Playlists()
