from dataclasses import dataclass
from typing import Any


@dataclass
class SimilarArtistEntry:
    artisthash: str
    name: str
    weight: float
    scrobbles: int
    listeners: int


@dataclass
class SimilarArtist:
    artisthash: str
    similar_artists: list[SimilarArtistEntry]


    def get_artist_hash_set(self) -> set[str]:
        """
        Returns a set of similar artists.
        """
        if not self.similar_artists:
            return set()

        # INFO: 
        return set(a['artisthash'] for a in self.similar_artists)
