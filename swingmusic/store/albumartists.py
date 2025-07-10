# swingmusic/store/albumartists.py
"""
Store for managing album artists (different from track artists).
Album artists represent the main artist(s) for an album, not individual track artists.
"""

from typing import Iterable
from collections import defaultdict

from swingmusic.models import Artist
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.hashing import create_hash
from swingmusic.store.tracks import TrackStore

ALBUMARTIST_LOAD_KEY = ""


class AlbumArtistMapEntry:
    def __init__(
        self, artist: Artist, albumhashes: set[str], trackhashes: set[str]
    ) -> None:
        self.artist = artist
        self.albumhashes: set[str] = albumhashes
        self.trackhashes: set[str] = trackhashes

    def increment_playcount(self, duration: int, timestamp: int, playcount: int = 1):
        self.artist.lastplayed = timestamp
        self.artist.playduration += duration
        self.artist.playcount += playcount

    def toggle_favorite_user(self, userid: int | None = None):
        if userid is None:
            userid = get_current_userid()

        self.artist.toggle_favorite_user(userid)

    def set_color(self, color: str):
        self.artist.color = color


class AlbumArtistStore:
    albumartistmap: dict[str, AlbumArtistMapEntry] = {}

    @classmethod
    def load_album_artists(cls, instance_key: str):
        """
        Loads all album artists from track data into the store.
        """
        global ALBUMARTIST_LOAD_KEY
        ALBUMARTIST_LOAD_KEY = instance_key

        print("Loading album artists... ", end="")
        cls.albumartistmap.clear()

        # Get all tracks to extract album artists
        tracks = TrackStore.get_flat_list()
        
        # Dictionary to aggregate data for each album artist
        album_artists_data = defaultdict(lambda: {
            'name': '',
            'albumhashes': set(),
            'trackhashes': set(),
            'albums': set(),
            'tracks': set(),
            'genres': [],
            'playcount': 0,
            'playduration': 0,
            'lastplayed': 0,
            'date': 0
        })

        # Process tracks to extract album artist information
        for track in tracks:
            if instance_key != ALBUMARTIST_LOAD_KEY:
                return

            # Process each album artist for this track
            for albumartist in track.albumartists:
                artisthash = albumartist['artisthash']
                artist_name = albumartist['name']
                
                # Update artist data
                artist_data = album_artists_data[artisthash]
                if not artist_data['name']:
                    artist_data['name'] = artist_name
                
                artist_data['albumhashes'].add(track.albumhash)
                artist_data['trackhashes'].add(track.trackhash)
                artist_data['albums'].add(track.albumhash)
                artist_data['tracks'].add(track.trackhash)
                
                # Aggregate genres
                if track.genres:
                    artist_data['genres'].extend(track.genres)
                
                # Aggregate play stats
                artist_data['playcount'] += track.playcount
                artist_data['playduration'] += track.playduration
                
                # Update last played timestamp
                if track.lastplayed > artist_data['lastplayed']:
                    artist_data['lastplayed'] = track.lastplayed
                
                # Update date (use earliest/oldest date)
                if artist_data['date'] == 0 or (track.date > 0 and track.date < artist_data['date']):
                    artist_data['date'] = track.date

        # Create Artist objects and populate the store
        for artisthash, data in album_artists_data.items():
            if instance_key != ALBUMARTIST_LOAD_KEY:
                return

            # Remove duplicate genres
            unique_genres = []
            seen_genres = set()
            for genre in data['genres']:
                if isinstance(genre, dict) and genre.get('genrehash') not in seen_genres:
                    unique_genres.append(genre)
                    seen_genres.add(genre['genrehash'])
                elif isinstance(genre, str) and genre not in seen_genres:
                    # Handle simple string genres
                    genre_hash = create_hash(genre)
                    unique_genres.append({'name': genre, 'genrehash': genre_hash})
                    seen_genres.add(genre_hash)

            # Create Artist object
            artist = Artist(
                artisthash=artisthash,
                name=data['name'],
                albumcount=len(data['albums']),
                trackcount=len(data['tracks']),
                playcount=data['playcount'],
                playduration=data['playduration'],
                lastplayed=data['lastplayed'],
                date=data['date'],
                genres=unique_genres,
                genrehashes=' '.join([g.get('genrehash', '') for g in unique_genres]),
                image='',  # Will be populated later if needed
                color='',  # Will be populated later if needed
                duration=0,  # Calculate if needed
                created_date=data['date']
            )

            # Add to store
            cls.albumartistmap[artisthash] = AlbumArtistMapEntry(
                artist=artist,
                albumhashes=data['albumhashes'],
                trackhashes=data['trackhashes']
            )

        print("Done!")

    @classmethod
    def get_flat_list(cls):
        """
        Returns a flat list of all album artists.
        """
        return [entry.artist for entry in cls.albumartistmap.values()]

    @classmethod
    def get_artist_by_hash(cls, artisthash: str) -> Artist | None:
        """
        Returns an album artist by its hash.
        """
        entry = cls.albumartistmap.get(artisthash)
        return entry.artist if entry else None

    @classmethod
    def get_artists_by_hashes(cls, artisthashes: Iterable[str]) -> list[Artist]:
        """
        Returns album artists by their hashes.
        """
        artists = []
        for artisthash in artisthashes:
            entry = cls.albumartistmap.get(artisthash)
            if entry is not None:
                artists.append(entry.artist)
        return artists

    @classmethod
    def get_album_artist_tracks(cls, artisthash: str):
        """
        Returns all tracks for a given album artist.
        """
        entry = cls.albumartistmap.get(artisthash)
        if entry is None:
            return []
        
        return TrackStore.get_tracks_by_trackhashes(entry.trackhashes)

    @classmethod
    def get_albums_by_artisthash(cls, artisthash: str):
        """
        Returns all albums for a given album artist.
        """
        from swingmusic.store.albums import AlbumStore
        
        entry = cls.albumartistmap.get(artisthash)
        if entry is None:
            return []
        
        return AlbumStore.get_albums_by_hashes(entry.albumhashes)

    @classmethod
    def search_album_artists(cls, query: str, limit: int = 50) -> list[Artist]:
        """
        Search album artists by name.
        """
        query_lower = query.lower()
        results = []
        
        for entry in cls.albumartistmap.values():
            if query_lower in entry.artist.name.lower():
                results.append(entry.artist)
                
        # Sort by name and limit results
        results.sort(key=lambda x: x.name.lower())
        return results[:limit]

    @classmethod
    def get_stats(cls) -> dict:
        """
        Get statistics about album artists.
        """
        return {
            'total_album_artists': len(cls.albumartistmap),
            'artists_with_albums': sum(1 for entry in cls.albumartistmap.values() if len(entry.albumhashes) > 0),
            'total_albums': sum(len(entry.albumhashes) for entry in cls.albumartistmap.values()),
            'total_tracks': sum(len(entry.trackhashes) for entry in cls.albumartistmap.values())
        }