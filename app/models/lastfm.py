from dataclasses import dataclass


@dataclass
class SimilarArtist:
    artisthash: str
    similar_artist_hashes: str

    def get_artist_hash_set(self) -> set[str]:
        """
        Returns a set of similar artists.
        """
        return set(self.similar_artist_hashes.split("~"))
