"""
This file contains the Artists class for interacting with artist documents in MongoDB.
"""
from app.db.mongodb import MongoArtists
from bson import ObjectId


class Artists(MongoArtists):
    """
    The artist class for all artist related database operations.
    """

    def insert_artist(self, artist_obj: dict) -> None:
        """
        Inserts an artist into the database.
        """
        self.collection.update_one(artist_obj, {
            "$set": artist_obj
        },
                                   upsert=True).upserted_id

    def get_all_artists(self) -> list:
        """
        Returns a list of all artists in the database.
        """
        return self.collection.find()

    def get_artist_by_id(self, artist_id: str) -> dict:
        """
        Returns an artist matching the mongo Id.
        """
        return self.collection.find_one({"_id": ObjectId(artist_id)})

    def get_artists_by_name(self, query: str):
        """
        Returns all the artists matching the query.
        """
        return self.collection.find({"name": query}).limit(20)
