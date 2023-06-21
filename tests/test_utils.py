# from hypothesis import given
from app.utils.parsers import parse_feat_from_title


def test_extract_featured_artists_from_title():
    test_titles = [
        "Own it (Featuring Ed Sheeran & Stormzy)",
        "Own it (Featuring Ed Sheeran and Stormzy)",
        "Autograph (On my line)(Feat. Lil Peep)(Deluxe)",
        "Why so sad? (with Juice Wrld, Lil Peep)",
        "Why so sad? (with Juice Wrld/Lil Peep)",
        "Simmer (with Burna Boy)",
        "Simmer (without Burna Boy)",
    ]

    results = [
        ["Ed Sheeran", "Stormzy"],
        ["Ed Sheeran", "Stormzy"],
        ["Lil Peep"],
        ["Juice Wrld", "Lil Peep"],
        ["Juice Wrld", "Lil Peep"],
        ["Burna Boy"],
        [],
    ]

    for title, expected in zip(test_titles, results):
        assert parse_feat_from_title(title)[0] == expected


# === HYPOTHESIS GHOSTWRITER TESTS ===

# @given(__dir=st.text(), full=st.booleans())
# def test_fuzz_run_fast_scandir(__dir: str, full) -> None:
#     app.utils.run_fast_scandir(_dir=__dir, full=full)
