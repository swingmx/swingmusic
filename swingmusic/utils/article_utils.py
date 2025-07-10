# swingmusic/utils/article_utils.py
"""
Utility functions for handling articles in artist and album names for sorting purposes.
"""

import re
from typing import List

# Common articles in various languages
ARTICLES = [
    # English
    "the", "a", "an",
    # Spanish
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    # French  
    "le", "la", "les", "un", "une", "des",
    # German
    "der", "die", "das", "ein", "eine", "einen", "einem", "einer",
    # Italian
    "il", "lo", "la", "gli", "le", "un", "uno", "una",
    # Portuguese
    "o", "a", "os", "as", "um", "uma", "uns", "umas",
    # Dutch
    "de", "het", "een",
]


def remove_articles_for_sorting(name: str) -> str:
    """
    Removes leading articles from a name for sorting purposes.
    
    Examples:
        "The Beatles" -> "Beatles"
        "A Perfect Circle" -> "Perfect Circle"
        "The B-52's" -> "B-52's"
        "Los Angeles" -> "Angeles"  # if it's actually an artist name
    
    Args:
        name: The artist or album name
        
    Returns:
        The name with leading articles removed, or the original name if no articles found
    """
    if not name or not isinstance(name, str):
        return name
    
    # Create pattern to match articles at the beginning of the string
    # followed by a space or hyphen
    articles_pattern = r'^(' + '|'.join(re.escape(article) for article in ARTICLES) + r')(\s+|-)'
    
    # Remove the article (case-insensitive)
    result = re.sub(articles_pattern, '', name.strip(), flags=re.IGNORECASE)
    
    # If result is empty or just whitespace, return original name
    return result.strip() if result.strip() else name


def get_sort_key(name: str) -> str:
    """
    Generate a sort key for a name by removing articles and converting to lowercase.
    
    Args:
        name: The name to generate a sort key for
        
    Returns:
        A normalized sort key
    """
    if not name:
        return ""
        
    # Remove articles and convert to lowercase for case-insensitive sorting
    return remove_articles_for_sorting(name).lower()


def get_artist_sort_key(artist_data) -> str:
    """
    Get sort key for artist data (handles both dict and object formats).
    
    Args:
        artist_data: Either an Artist object with .name attribute or dict with 'name' key
        
    Returns:
        Sort key for the artist
    """
    if hasattr(artist_data, 'name'):
        return get_sort_key(artist_data.name)
    elif isinstance(artist_data, dict) and 'name' in artist_data:
        return get_sort_key(artist_data['name'])
    else:
        return ""


# Test cases for validation
if __name__ == "__main__":
    test_cases = [
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
    ]
    
    print("Testing article removal:")
    for input_name, expected in test_cases:
        result = remove_articles_for_sorting(input_name)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{input_name}' -> '{result}' (expected: '{expected}')")