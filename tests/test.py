from app.utils import extract_featured_artists_from_title


def test_extract_featured_artists_from_title():
    test_titles = [
        "Own it (Featuring Ed Sheeran & Stormzy)",
        "Godzilla (Deluxe)(Feat. Juice Wrld)(Deluxe)",
        "Simmer (with Burna Boy)",
    ]

    expected_test_artists = [
        ["Ed Sheeran", "Stormzy"],
        ['Juice Wrld'],
        ["Burna Boy"]
    ]

    for title, expected in zip(test_titles, expected_test_artists):
        assert extract_featured_artists_from_title(title) == expected
