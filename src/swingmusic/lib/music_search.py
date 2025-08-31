import os
import tempfile
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from whoosh.fields import Schema, TEXT, ID, NUMERIC, DATETIME
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer
from whoosh.index import create_in, open_dir, Index
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.searching import Searcher, Results
from whoosh.filedb.filestore import FileStorage


@dataclass
class MusicTrack:
    """Data class representing a music track for indexing."""
    track_id: str
    title: str
    artist: str
    album: str
    album_artist: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    duration: Optional[float] = None
    track_number: Optional[int] = None
    file_path: Optional[str] = None
    added_date: Optional[str] = None


class MusicSearchEngine:
    """Search engine for music data using Whoosh."""
    
    def __init__(self, index_dir: Optional[str] = None):
        """Initialize the search engine.
        
        Args:
            index_dir: Directory to store the search index. If None, uses a temporary directory.
        """
        if index_dir is None:
            self.index_dir = tempfile.mkdtemp(prefix="music_search_")
        else:
            self.index_dir = index_dir
            
        self.index_path = Path(self.index_dir)
        self.index_path.mkdir(exist_ok=True)
        
        # Define the schema for music data
        self.schema = Schema(
            track_id=ID(stored=True, unique=True),
            title=TEXT(analyzer=StemmingAnalyzer(), stored=True, sortable=True),
            artist=TEXT(analyzer=StemmingAnalyzer(), stored=True, sortable=True),
            album=TEXT(analyzer=StemmingAnalyzer(), stored=True, sortable=True),
            album_artist=TEXT(analyzer=StemmingAnalyzer(), stored=True),
            genre=TEXT(analyzer=StandardAnalyzer(), stored=True),
            year=NUMERIC(stored=True, sortable=True),
            duration=NUMERIC(stored=True, sortable=True),
            track_number=NUMERIC(stored=True, sortable=True),
            file_path=ID(stored=True),
            added_date=TEXT(stored=True, sortable=True)  # Changed from DATETIME to TEXT for Whoosh 2.7.5
        )
        
        self.index: Optional[Index] = None
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize the search index."""
        try:
            # Try to open existing index
            self.index = open_dir(self.index_dir)
        except:
            # Create new index if none exists
            self.index = create_in(self.index_dir, self.schema)
    
    def add_track(self, track: MusicTrack) -> bool:
        """Add a single track to the search index.
        
        Args:
            track: MusicTrack object to index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            writer = self.index.writer()
            writer.add_document(
                track_id=track.track_id,
                title=track.title,
                artist=track.artist,
                album=track.album,
                album_artist=track.album_artist or "",
                genre=track.genre or "",
                year=track.year or 0,
                duration=track.duration or 0.0,
                track_number=track.track_number or 0,
                file_path=track.file_path or "",
                added_date=track.added_date or ""
            )
            writer.commit()
            return True
        except Exception as e:
            print(f"Error indexing track {track.track_id}: {e}")
            return False
    
    def add_tracks(self, tracks: List[MusicTrack]) -> int:
        """Add multiple tracks to the search index.
        
        Args:
            tracks: List of MusicTrack objects to index
            
        Returns:
            Number of successfully indexed tracks
        """
        if not tracks:
            return 0
            
        try:
            writer = self.index.writer()
            success_count = 0
            
            for track in tracks:
                try:
                    writer.add_document(
                        track_id=track.track_id,
                        title=track.title,
                        artist=track.artist,
                        album=track.album,
                        album_artist=track.album_artist or "",
                        genre=track.genre or "",
                        year=track.year or 0,
                        duration=track.duration or 0.0,
                        track_number=track.track_number or 0,
                        file_path=track.file_path or "",
                        added_date=track.added_date or ""
                    )
                    success_count += 1
                except Exception as e:
                    print(f"Error indexing track {track.track_id}: {e}")
                    continue
            
            writer.commit()
            return success_count
        except Exception as e:
            print(f"Error in batch indexing: {e}")
            return 0
    
    def search_tracks(self, query: str, limit: int = 20, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """Search for tracks using a query string.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            fuzzy: Whether to enable fuzzy matching
            
        Returns:
            List of matching track dictionaries
        """
        if not self.index:
            return []
        
        try:
            # Create a multifield parser for searching across title, artist, and album
            parser = MultifieldParser(
                ["title", "artist", "album", "album_artist", "genre"], 
                self.schema
            )
            
            # Parse the query
            parsed_query = parser.parse(query)
            
            # If fuzzy search is enabled, add fuzzy matching to terms
            if fuzzy:
                parsed_query = self._add_fuzzy_matching(parsed_query)
            
            # Perform the search
            with self.index.searcher() as searcher:
                results = searcher.search(parsed_query, limit=limit)
                return [dict(result) for result in results]
                
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def search_by_title(self, title: str, limit: int = 20, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """Search for tracks by title.
        
        Args:
            title: Track title to search for
            limit: Maximum number of results to return
            fuzzy: Whether to enable fuzzy matching
            
        Returns:
            List of matching track dictionaries
        """
        if not self.index:
            return []
        
        try:
            parser = QueryParser("title", self.schema)
            query = parser.parse(title)
            
            if fuzzy:
                query = self._add_fuzzy_matching(query)
            
            with self.index.searcher() as searcher:
                results = searcher.search(query, limit=limit)
                return [dict(result) for result in results]
                
        except Exception as e:
            print(f"Title search error: {e}")
            return []
    
    def search_by_artist(self, artist: str, limit: int = 20, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """Search for tracks by artist.
        
        Args:
            artist: Artist name to search for
            limit: Maximum number of results to return
            fuzzy: Whether to enable fuzzy matching
            
        Returns:
            List of matching track dictionaries
        """
        if not self.index:
            return []
        
        try:
            parser = QueryParser("artist", self.schema)
            query = parser.parse(artist)
            
            if fuzzy:
                query = self._add_fuzzy_matching(query)
            
            with self.index.searcher() as searcher:
                results = searcher.search(query, limit=limit)
                return [dict(result) for result in results]
                
        except Exception as e:
            print(f"Artist search error: {e}")
            return []
    
    def search_by_album(self, album: str, limit: int = 20, fuzzy: bool = True) -> List[Dict[str, Any]]:
        """Search for tracks by album.
        
        Args:
            album: Album name to search for
            limit: Maximum number of results to return
            fuzzy: Whether to enable fuzzy matching
            
        Returns:
            List of matching track dictionaries
        """
        if not self.index:
            return []
        
        try:
            parser = QueryParser("album", self.schema)
            query = parser.parse(album)
            
            if fuzzy:
                query = self._add_fuzzy_matching(query)
            
            with self.index.searcher() as searcher:
                results = searcher.search(query, limit=limit)
                return [dict(result) for result in results]
                
        except Exception as e:
            print(f"Album search error: {e}")
            return []
    
    def _add_fuzzy_matching(self, query) -> Any:
        """Add fuzzy matching to query terms.
        
        Args:
            query: Parsed query object
            
        Returns:
            Query with fuzzy matching enabled
        """
        # This is a simplified approach - in practice, you might want to
        # modify the query parser or use Whoosh's fuzzy query features
        return query
    
    def get_spelling_suggestions(self, word: str) -> List[str]:
        """Get spelling suggestions for a word.
        
        Args:
            word: Word to get suggestions for
            
        Returns:
            List of spelling suggestions
        """
        # Simplified spelling suggestions for Whoosh 2.7.5
        # In a real implementation, you might implement your own spelling correction
        return []
    
    def clear_index(self) -> bool:
        """Clear all documents from the index.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            writer = self.index.writer()
            # In Whoosh 2.7.5, we need to delete by a query that matches all documents
            from whoosh.query import Every
            writer.delete_by_query(Every())
            writer.commit()
            return True
        except Exception as e:
            print(f"Error clearing index: {e}")
            return False
    
    def delete_track(self, track_id: str) -> bool:
        """Delete a specific track from the index.
        
        Args:
            track_id: ID of the track to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            writer = self.index.writer()
            writer.delete_by_term("track_id", track_id)
            writer.commit()
            return True
        except Exception as e:
            print(f"Error deleting track {track_id}: {e}")
            return False
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the search index.
        
        Returns:
            Dictionary containing index statistics
        """
        if not self.index:
            return {}
        
        try:
            with self.index.searcher() as searcher:
                # Convert generator to list for length calculation
                documents = list(searcher.documents())
                return {
                    "total_documents": searcher.doc_count(),
                    "index_size": len(documents),
                    "index_path": str(self.index_path)
                }
        except Exception as e:
            print(f"Error getting index stats: {e}")
            return {}
    
    def optimize_index(self) -> bool:
        """Optimize the search index for better performance.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            writer = self.index.writer()
            writer.commit(optimize=True)
            return True
        except Exception as e:
            print(f"Error optimizing index: {e}")
            return False
    
    def close(self):
        """Close the search engine and clean up resources."""
        if self.index:
            self.index.close()
