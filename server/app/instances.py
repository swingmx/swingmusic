"""
All the MongoDB instances are created here.
"""

from app.db import artists, albums, trackcolors, tracks, playlists

songs_instance = tracks.AllSongs()
artist_instance = artists.Artists()
track_color_instance = trackcolors.TrackColors()
album_instance = albums.Albums()
playlist_instance = playlists.Playlists()