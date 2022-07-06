"""
This file contains the Album class for interacting with
album documents in MongoDB.
"""
from typing import List

from app.db.mongodb import convert_many
from app.db.mongodb import convert_one
from app.db.mongodb import MongoAlbums
from app.models import Album
from bson import ObjectId


class Albums(MongoAlbums):
    """
    The class for all album-related database operations.
    """

    def insert_album(self, album: Album) -> None:
        """
        Inserts a new album object into the database.
        """
        album = album.__dict__
        return self.collection.update_one(
            {
                "album": album["title"],
                "artist": album["artist"]
            },
            {
                "$set": album
            },
            upsert=True,
        ).upserted_id

    def insert_many(self, albums: Album):
        albums = [a.__dict__ for a in albums]
        """
        Inserts multiple albums into the database.
        """
        return self.collection.insert_many(albums)

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

    def find_album_by_hash(self, hash: str) -> dict:
        """
        Returns a single album matching the hash in the query params.
        """
        album = self.collection.find_one({"hash": hash})
        return convert_one(album)

    def set_album_colors(self, colors: List[str], hash: str) -> None:
        """
        Sets the colors for an album.
        """
        self.collection.update_one(
            {"hash": hash},
            {"$set": {
                "colors": colors
            }},
        )
