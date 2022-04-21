"""
All the MongoDB instances are created here.
"""
from app.db import albums
from app.db import artists
from app.db import playlists
from app.db import trackcolors
from app.db import tracks

tracks_instance = tracks.AllSongs()
artist_instance = artists.Artists()
track_color_instance = trackcolors.TrackColors()
album_instance = albums.Albums()
playlist_instance = playlists.Playlists()
