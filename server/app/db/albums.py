"""
This file contains the Album class for interacting with 
album documents in MongoDB.
"""

from app import db
from bson import ObjectId

convert_many = db.convert_many
convert_one = db.convert_one


class Albums(db.Mongo):
    """
    The class for all album-related database operations.
    """

    def __init__(self):
        super(Albums, self).__init__("ALICE_ALBUMS")
        self.collection = self.db["ALL_ALBUMS"]

    def insert_album(self, album: dict) -> None:
        """
        Inserts a new album object into the database.
        """
        return self.collection.update_one(
            {"album": album["album"], "artist": album["artist"]},
            {"$set": album},
            upsert=True,
        ).upserted_id

    def get_all_albums(self) -> list:
        """
        Returns all the albums in the database.
        """
        albums = self.collection.find()
        return convert_many(albums)

    def get_album_by_id(self, id: str) -> dict:
        """
        Returns a single album matching the id in the query params.
        """
        album = self.collection.find_one({"_id": ObjectId(id)})
        return convert_one(album)

    def get_album_by_name(self, name: str, artist: str) -> dict:
        """
        Returns a single album matching the name in the query params.
        """
        album = self.collection.find_one({"album": name, "artist": artist})
        return convert_one(album)

    def get_album_by_artist(self, name: str) -> dict:
        """
        Returns a single album matching the artist in the query params.
        """
        album = self.collection.find_one({"albumartist": name})
        return convert_one(album)
