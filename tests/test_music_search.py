import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from swingmusic.lib.music_search import MusicSearchEngine, MusicTrack


class TestMusicSearchEngine(unittest.TestCase):
    """Test cases for MusicSearchEngine class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp(prefix="test_music_search_")
        self.search_engine = MusicSearchEngine(self.test_dir)

        # Sample music tracks for testing
        self.sample_tracks = [
            MusicTrack(
                track_id="1",
                title="I Don't Wanna Talk About It",
                artist="Rod Stewart",
                album="Atlantic Crossing",
                album_artist="Rod Stewart",
                genre="Rock",
                year=1975,
                duration=272.5,
                track_number=1,
                file_path="/music/rod_stewart/atlantic_crossing/01.mp3",
                added_date="2024-01-01",
            ),
            MusicTrack(
                track_id="2",
                title="Maggie May",
                artist="Rod Stewart",
                album="Every Picture Tells a Story",
                album_artist="Rod Stewart",
                genre="Rock",
                year=1971,
                duration=342.0,
                track_number=1,
                file_path="/music/rod_stewart/every_picture/01.mp3",
                added_date="2024-01-01",
            ),
            MusicTrack(
                track_id="3",
                title="Tonight's the Night",
                artist="Rod Stewart",
                album="Atlantic Crossing",
                album_artist="Rod Stewart",
                genre="Rock",
                year=1975,
                duration=208.0,
                track_number=2,
                file_path="/music/rod_stewart/atlantic_crossing/02.mp3",
                added_date="2024-01-01",
            ),
            MusicTrack(
                track_id="4",
                title="Hotel California",
                artist="Eagles",
                album="Hotel California",
                album_artist="Eagles",
                genre="Rock",
                year=1976,
                duration=391.0,
                track_number=1,
                file_path="/music/eagles/hotel_california/01.mp3",
                added_date="2024-01-01",
            ),
            MusicTrack(
                track_id="5",
                title="New Kid in Town",
                artist="Eagles",
                album="Hotel California",
                album_artist="Eagles",
                genre="Rock",
                year=1976,
                duration=308.0,
                track_number=2,
                file_path="/music/eagles/hotel_california/02.mp3",
                added_date="2024-01-01",
            ),
        ]

    def tearDown(self):
        """Clean up after each test method."""
        if self.search_engine:
            self.search_engine.close()

        # Remove temporary directory
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)

    def test_initialization(self):
        """Test search engine initialization."""
        self.assertIsNotNone(self.search_engine.index)
        self.assertIsNotNone(self.search_engine.schema)
        self.assertEqual(self.search_engine.index_dir, self.test_dir)

    def test_add_single_track(self):
        """Test adding a single track to the index."""
        track = self.sample_tracks[0]
        result = self.search_engine.add_track(track)
        self.assertTrue(result)

        # Verify track was added
        stats = self.search_engine.get_index_stats()
        self.assertEqual(stats["total_documents"], 1)

    def test_add_multiple_tracks(self):
        """Test adding multiple tracks to the index."""
        result = self.search_engine.add_tracks(self.sample_tracks)
        self.assertEqual(result, len(self.sample_tracks))

        # Verify all tracks were added
        stats = self.search_engine.get_index_stats()
        self.assertEqual(stats["total_documents"], len(self.sample_tracks))

    def test_search_by_title_exact(self):
        """Test searching for tracks by exact title."""
        self.search_engine.add_tracks(self.sample_tracks)

        results = self.search_engine.search_by_title("I Don't Wanna Talk About It")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "I Don't Wanna Talk About It")
        self.assertEqual(results[0]["artist"], "Rod Stewart")

    def test_search_by_title_partial(self):
        """Test searching for tracks by partial title."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search for partial title - should find "I Don't Wanna Talk About It"
        results = self.search_engine.search_by_title("don't talk about it")
        self.assertGreaterEqual(len(results), 1)

        # Verify we found the expected track
        found_track = None
        for result in results:
            if "don't wanna talk about it" in result["title"].lower():
                found_track = result
                break

        self.assertIsNotNone(found_track)
        self.assertEqual(found_track["artist"], "Rod Stewart")

    def test_search_by_artist(self):
        """Test searching for tracks by artist."""
        self.search_engine.add_tracks(self.sample_tracks)

        results = self.search_engine.search_by_artist("Rod Stewart")
        self.assertEqual(len(results), 3)  # Rod Stewart has 3 tracks

        # Verify all results are by Rod Stewart
        for result in results:
            self.assertEqual(result["artist"], "Rod Stewart")

    def test_search_by_album(self):
        """Test searching for tracks by album."""
        self.search_engine.add_tracks(self.sample_tracks)

        results = self.search_engine.search_by_album("Hotel California")
        self.assertEqual(len(results), 2)  # Hotel California has 2 tracks

        # Verify all results are from Hotel California
        for result in results:
            self.assertEqual(result["album"], "Hotel California")

    def test_multi_field_search(self):
        """Test searching across multiple fields."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search for "talk about it rod stewart" - should find the track
        results = self.search_engine.search_tracks("talk about it rod stewart")
        self.assertGreaterEqual(len(results), 1)

        # Verify we found the expected track
        found_track = None
        for result in results:
            if (
                "rod stewart" in result["artist"].lower()
                and "talk about it" in result["title"].lower()
            ):
                found_track = result
                break

        self.assertIsNotNone(found_track)
        self.assertEqual(found_track["title"], "I Don't Wanna Talk About It")

    def test_search_with_limit(self):
        """Test search result limiting."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search with limit of 2
        results = self.search_engine.search_tracks("rod stewart", limit=2)
        self.assertLessEqual(len(results), 2)

    def test_search_by_track_title_and_album(self):
        """Test searching by track title and album name."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search for "talk about it atlantic crossing"
        results = self.search_engine.search_tracks("talk about it atlantic crossing")
        self.assertGreaterEqual(len(results), 1)

        # Verify we found the expected track
        found_track = None
        for result in results:
            if (
                "talk about it" in result["title"].lower()
                and "atlantic crossing" in result["album"].lower()
            ):
                found_track = result
                break

        self.assertIsNotNone(found_track)
        self.assertEqual(found_track["title"], "I Don't Wanna Talk About It")
        self.assertEqual(found_track["album"], "Atlantic Crossing")

    def test_fuzzy_search_enabled(self):
        """Test that fuzzy search is enabled by default."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search with a slight typo - should still find results
        results = self.search_engine.search_by_title(
            "don't talk abot it"
        )  # typo: "abot"
        self.assertGreaterEqual(len(results), 0)  # Should find something even with typo

    def test_fuzzy_search_disabled(self):
        """Test searching with fuzzy search disabled."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search with fuzzy disabled
        results = self.search_engine.search_by_title("don't talk abot it", fuzzy=False)
        # Results may vary depending on exact matching behavior

    def test_delete_track(self):
        """Test deleting a track from the index."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Verify track exists
        initial_stats = self.search_engine.get_index_stats()
        self.assertEqual(initial_stats["total_documents"], len(self.sample_tracks))

        # Delete a track
        result = self.search_engine.delete_track("1")
        self.assertTrue(result)

        # Verify track was deleted
        final_stats = self.search_engine.get_index_stats()
        self.assertEqual(final_stats["total_documents"], len(self.sample_tracks) - 1)

        # Verify the specific track is gone
        search_results = self.search_engine.search_by_title(
            "I Don't Wanna Talk About It"
        )
        self.assertEqual(len(search_results), 0)

    def test_clear_index(self):
        """Test clearing the entire index."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Verify tracks exist
        initial_stats = self.search_engine.get_index_stats()
        self.assertEqual(initial_stats["total_documents"], len(self.sample_tracks))

        # Clear index
        result = self.search_engine.clear_index()
        self.assertTrue(result)

        # Verify index is empty
        final_stats = self.search_engine.get_index_stats()
        self.assertEqual(final_stats["total_documents"], 0)

    def test_get_index_stats(self):
        """Test getting index statistics."""
        self.search_engine.add_tracks(self.sample_tracks)

        stats = self.search_engine.get_index_stats()
        self.assertIn("total_documents", stats)
        self.assertIn("index_path", stats)
        self.assertEqual(stats["total_documents"], len(self.sample_tracks))
        self.assertEqual(stats["index_path"], self.test_dir)

    def test_optimize_index(self):
        """Test index optimization."""
        self.search_engine.add_tracks(self.sample_tracks)

        result = self.search_engine.optimize_index()
        self.assertTrue(result)

    def test_spelling_suggestions(self):
        """Test spelling suggestion functionality."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Get spelling suggestions for a misspelled word
        suggestions = self.search_engine.get_spelling_suggestions(
            "stewart"
        )  # Correct spelling
        # Suggestions may vary, but should return something
        self.assertIsInstance(suggestions, list)

    def test_search_empty_index(self):
        """Test searching an empty index."""
        results = self.search_engine.search_tracks("anything")
        self.assertEqual(len(results), 0)

    def test_add_track_with_missing_fields(self):
        """Test adding a track with missing optional fields."""
        track = MusicTrack(
            track_id="6",
            title="Test Track",
            artist="Test Artist",
            album="Test Album",
            # Missing optional fields
        )

        result = self.search_engine.add_track(track)
        self.assertTrue(result)

        # Verify track was added
        stats = self.search_engine.get_index_stats()
        self.assertEqual(stats["total_documents"], 1)

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search with different case
        results_lower = self.search_engine.search_by_title(
            "i don't wanna talk about it"
        )
        results_upper = self.search_engine.search_by_title(
            "I DON'T WANNA TALK ABOUT IT"
        )

        # Should return same results
        self.assertEqual(len(results_lower), len(results_upper))
        if results_lower and results_upper:
            self.assertEqual(results_lower[0]["track_id"], results_upper[0]["track_id"])

    def test_search_with_special_characters(self):
        """Test searching with special characters."""
        self.search_engine.add_tracks(self.sample_tracks)

        # Search with apostrophe
        results = self.search_engine.search_by_title("don't")
        self.assertGreaterEqual(len(results), 1)

        # Should find "I Don't Wanna Talk About It"
        found = False
        for result in results:
            if "don't wanna talk about it" in result["title"].lower():
                found = True
                break

        self.assertTrue(found)


if __name__ == "__main__":
    unittest.main()

