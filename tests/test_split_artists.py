import unittest

def split_artists(src: str, separators: set[str], ignoreList: set[str] = set()):
    """
    Splits a string of artists into a list of artists, preserving those in ignoreList.
    Case-insensitive matching is used for the ignoreList.
    """
    result = []
    current = ""
    i = 0
    
    # Convert ignoreList to lowercase for case-insensitive matching
    ignore_lower = {artist.lower() for artist in ignoreList}
    
    while i < len(src):
        # Check if any ignored artist starts at this position (case-insensitive)
        ignored_match = next(
            (
                src[i:i+len(ignored)] 
                for ignored in ignoreList 
                if src.lower().startswith(ignored.lower(), i)
            ), 
            None
        )
        
        if ignored_match:
            # If we have accumulated any current string, add it to result
            if current.strip():
                result.extend([a.strip() for a in current.split(',') if a.strip()])
                current = ""
            # Add the ignored artist to the result (preserving original case)
            result.append(ignored_match)
            # Move past the ignored artist
            i += len(ignored_match)
        elif src[i] in separators:
            # If we encounter a separator, process the current string
            if current.strip():
                result.extend([a.strip() for a in current.split(',') if a.strip()])
                current = ""
            i += 1
        else:
            # If it's not an ignored artist or a separator, add to current
            current += src[i]
            i += 1
    
    # Process any remaining current string
    if current.strip():
        result.extend([a.strip() for a in current.split(',') if a.strip()])
    
    return result


class TestSplitArtists(unittest.TestCase):

    def test_basic_splitting(self):
        self.assertEqual(
            split_artists("Beatles, Queen; Rolling Stones", {";"}),
            ["Beatles", "Queen", "Rolling Stones"],
        )

    def test_multiple_separators(self):
        self.assertEqual(
            split_artists("Beatles; Queen & Rolling Stones | ABBA", {";", "&", "|"}),
            ["Beatles", "Queen", "Rolling Stones", "ABBA"],
        )

    def test_ignore_list(self):
        self.assertEqual(
            split_artists(
                "Beatles; Earth, Wind & Fire; Queen", {";", "&"}, {"Earth, Wind & Fire"}
            ),
            ["Beatles", "Earth, Wind & Fire", "Queen"],
        )

    def test_empty_string(self):
        self.assertEqual(split_artists("", {";"}), [])

    def test_only_separators(self):
        self.assertEqual(split_artists(";;;", {";"}), [])

    def test_extra_spaces(self):
        self.assertEqual(
            split_artists("  Beatles  ;  Queen  ", {";"}), ["Beatles", "Queen"]
        )

    def test_comma_splitting(self):
        self.assertEqual(
            split_artists("Beatles, Queen; Rolling Stones, ABBA", {";"}),
            ["Beatles", "Queen", "Rolling Stones", "ABBA"],
        )

    def test_ignore_list_with_comma(self):
        self.assertEqual(
            split_artists(
                "Beatles; Earth, Wind & Fire, Queen", {";"}, {"Earth, Wind & Fire"}
            ),
            ["Beatles", "Earth, Wind & Fire", "Queen"],
        )

    def test_ignore_list_with_separator(self):
        self.assertEqual(
            split_artists("Beatles; AC/DC", {"/", ";"}, {"AC/DC"}), ["Beatles", "AC/DC"]
        )

    def test_ignore_list_at_start(self):
        self.assertEqual(
            split_artists("AC/DC; Beatles", {"/", ";"}, {"AC/DC"}), ["AC/DC", "Beatles"]
        )

    def test_ignore_list_at_end(self):
        self.assertEqual(
            split_artists("Beatles; AC/DC", {"/", ";"}, {"AC/DC"}), ["Beatles", "AC/DC"]
        )

    def test_multiple_ignored_artists(self):
        self.assertEqual(
            split_artists(
                "Beatles; AC/DC; Guns N' Roses; Queen",
                {"/", ";", "'"},
                {"AC/DC", "Guns N' Roses"},
            ),
            ["Beatles", "AC/DC", "Guns N' Roses", "Queen"],
        )

    def test_bob_marley(self):
        self.assertEqual(
            split_artists(
                "Bob marley & The wailers; Beatles",
                {";", "&"},
                {"Bob marley & the wailers"},
            ),
            ["Bob marley & The wailers", "Beatles"],
        )


if __name__ == "__main__":
    unittest.main()
