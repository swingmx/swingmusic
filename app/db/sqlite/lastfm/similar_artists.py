from app.models.lastfm import SimilarArtist

from ..utils import SQLiteManager


class SQLiteLastFMSimilarArtists:
    """
    This class contains methods for interacting with the lastfm_similar_artists table.
    """

    @classmethod
    def insert_one(cls, artist: SimilarArtist):
        """
        Inserts a single artist into the database.
        """
        sql = """INSERT OR REPLACE INTO lastfm_similar_artists(artisthash, similar_artists) VALUES(?,?)"""

        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (artist.artisthash, artist.similar_artist_hashes))
            cur.close()

    @classmethod
    def get_similar_artists_for(cls, artisthash: str):
        """
        Returns a list of similar artists.
        """
        sql = """SELECT * FROM lastfm_similar_artists WHERE artisthash = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (artisthash,))
            similar_artists = cur.fetchone()
            cur.close()

            if similar_artists is None:
                return None

            return SimilarArtist(artisthash, similar_artists[2])

    @classmethod
    def get_all(cls):
        """
        Returns a list of all similar artists.
        """
        sql = """SELECT * FROM lastfm_similar_artists"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql)
            similar_artists = cur.fetchall()
            cur.close()

            for a in similar_artists:
                yield SimilarArtist(a[1], a[2])

    @classmethod
    def exists(cls, artisthash: str):
        """
        Checks if an artist exists in the database by counting the number of rows
        """
        sql = """SELECT COUNT(*) FROM lastfm_similar_artists WHERE artisthash = ?"""
        with SQLiteManager(userdata_db=True) as cur:
            cur.execute(sql, (artisthash,))
            count = cur.fetchone()[0]
            cur.close()
            return count > 0
