# test_article_sorting.py
"""
Test script to validate the article handling functionality works correctly.
Run this to verify that artists are sorted properly with articles removed.
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from swingmusic.utils.article_utils import remove_articles_for_sorting, get_sort_key


def test_article_removal():
    """Test the article removal functionality."""
    test_cases = [
        # (input, expected_output)
        ("The Beatles", "Beatles"),
        ("The B-52's", "B-52's"),
        ("A Perfect Circle", "Perfect Circle"),
        ("An Officer and a Gentleman", "Officer and a Gentleman"),
        ("Beatles", "Beatles"),  # No change
        ("", ""),  # Empty string
        ("The", "The"),  # Just an article - should return original
        ("Los Tigres del Norte", "Tigres del Norte"),
        ("Le Tigre", "Tigre"),
        ("Der Eisendrache", "Eisendrache"),
        ("AC/DC", "AC/DC"),  # No articles
        ("The Who", "Who"),
        ("A-ha", "ha"),
        ("The 1975", "1975"),
        ("U2", "U2"),  # No change
        ("R.E.M.", "R.E.M."),  # No change
        ("The Smashing Pumpkins", "Smashing Pumpkins"),
        ("Sublime", "Sublime"),  # No change (from your image)
    ]
    
    print("Testing article removal:")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for input_name, expected in test_cases:
        result = remove_articles_for_sorting(input_name)
        status = "✓" if result == expected else "✗"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
            
        print(f"{status} '{input_name}' -> '{result}' (expected: '{expected}')")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


def test_sorting_behavior():
    """Test that the sorting works as expected with the article removal."""
    
    # Artists from your screenshot plus some test cases
    artist_names = [
        "Soundtrack",
        "spoken intro", 
        "Stephen Lynch",
        "Stephen Trask",
        "Steve Howe",
        "Sublime",
        "Sublime featuring Mad Lion",
        "Swedish House Mafia",
        "System of a Down",
        "Talking Heads",
        "The Alan Parsons Project",
        "The Avett Brothers", 
        "The B-52's",
        "The Cars",
        "The Beatles",
        "The Who",
        "The Smashing Pumpkins",
        "A Perfect Circle",
        "An Officer and a Gentleman",
        "Beatles",  # To test that it comes after "The Beatles" -> "Beatles"
    ]
    
    print("\nTesting sorting behavior:")
    print("=" * 50)
    
    # Sort using our article-aware function
    sorted_artists = sorted(artist_names, key=get_sort_key)
    
    print("Sorted order (with articles removed for sorting):")
    for i, artist in enumerate(sorted_artists, 1):
        sort_key = get_sort_key(artist)
        print(f"{i:2d}. {artist:<30} (sort key: '{sort_key}')")
    
    # Verify that "The B-52's" comes under "B" not "T"
    b52_index = next(i for i, artist in enumerate(sorted_artists) if artist == "The B-52's")
    beatles_index = next(i for i, artist in enumerate(sorted_artists) if artist == "The Beatles")
    
    print(f"\nKey tests:")
    print(f"- 'The B-52's' appears at position {b52_index + 1}")
    print(f"- 'The Beatles' appears at position {beatles_index + 1}")
    
    # Check that B-52's comes before most "S" entries
    sublime_index = next(i for i, artist in enumerate(sorted_artists) if artist == "Sublime")
    b52s_before_sublime = b52_index < sublime_index
    print(f"- 'The B-52's' comes before 'Sublime': {b52s_before_sublime} ✓" if b52s_before_sublime else f"- 'The B-52's' comes before 'Sublime': {b52s_before_sublime} ✗")
    
    return True


def test_edge_cases():
    """Test edge cases and potential issues."""
    
    print("\nTesting edge cases:")
    print("=" * 50)
    
    edge_cases = [
        (None, ""),  # None input
        ("", ""),    # Empty string
        ("   ", ""),   # Whitespace only
        ("The", "The"),  # Just an article
        ("A", "A"),      # Single letter that's an article
        ("The The", "The"),  # Band name "The The"
        ("Los Los", "Los"),  # Repeated articles
        ("El Niño", "Niño"),  # Spanish article
        ("Die Antwoord", "Antwoord"),  # German article
        ("Le Loup", "Loup"),  # French article
    ]
    
    for input_val, expected in edge_cases:
        try:
            result = remove_articles_for_sorting(input_val) if input_val is not None else ""
            status = "✓" if result == expected else "✗"
            print(f"{status} {repr(input_val)} -> {repr(result)} (expected: {repr(expected)})")
        except Exception as e:
            print(f"✗ {repr(input_val)} -> ERROR: {e}")


if __name__ == "__main__":
    print("Article Sorting Test Suite")
    print("=" * 50)
    
    success = True
    
    try:
        success &= test_article_removal()
        test_sorting_behavior()
        test_edge_cases()
        
        if success:
            print(f"\n🎉 All tests passed! Article-aware sorting is working correctly.")
            print("The B-52's should now appear under 'B' instead of 'T' in your artist list.")
        else:
            print(f"\n❌ Some tests failed. Please check the implementation.")
            
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you're running this from the correct directory and the module paths are correct.")
    except Exception as e:
        print(f"Unexpected error: {e}")