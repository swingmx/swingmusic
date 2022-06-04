"""
All the MongoDB instances are created here.
"""
from app.db.mongodb import albums, artists, playlists, tracks

tracks_instance = tracks.Tracks()
artist_instance = artists.Artists()
album_instance = albums.Albums()
playlist_instance = playlists.Playlists()
