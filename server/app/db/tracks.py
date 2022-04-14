"""
This file contains the AllSongs class for interacting with track documents in MongoDB.
"""

from app import db
from bson import ObjectId

convert_many = db.convert_many
convert_one = db.convert_one


class AllSongs(db.Mongo):
    """
    The class for all track-related database operations.
    """

    def __init__(self):
        super(AllSongs, self).__init__("ALICE_MUSIC_TRACKS")
        self.collection = self.db["ALL_TRACKS"]

    # def drop_db(self):
    #     self.collection.drop()

    def insert_song(self, song_obj: dict) -> str:
        """
        Inserts a new track object into the database.
        """
        return self.collection.update_one(
            {"filepath": song_obj["filepath"]}, {"$set": song_obj}, upsert=True
        ).upserted_id

    def get_all_songs(self) -> list:
        """
        Returns all tracks in the database.
        """
        return convert_many(self.collection.find())

    def get_song_by_id(self, file_id: str) -> dict:
        """
        Returns a track object by its mongodb id.
        """
        song = self.collection.find_one({"_id": ObjectId(file_id)})
        return convert_one(song)

    def get_song_by_album(self, name: str, artist: str) -> dict:
        """
        Returns a single track matching the album in the query params.
        """
        song = self.collection.find_one({"album": name, "albumartist": artist})
        return convert_one(song)

    def search_songs_by_album(self, query: str) -> list:
        """
        Returns all the songs matching the albums in the query params (using regex).
        """
        songs = self.collection.find(
            {"album": {"$regex": query, "$options": "i"}})
        return convert_many(songs)

    def search_songs_by_artist(self, query: str) -> list:
        """
        Returns all the songs matching the artists in the query params.
        """
        songs = self.collection.find(
            {"artists": {"$regex": query, "$options": "i"}})
        return convert_many(songs)

    def find_song_by_title(self, query: str) -> list:
        """
        Finds all the tracks matching the title in the query params.
        """
        song = self.collection.find(
            {"title": {"$regex": query, "$options": "i"}})
        return convert_many(song)

    def find_songs_by_album(self, name: str, artist: str) -> list:
        """
        Returns all the tracks exactly matching the album in the query params.
        """
        songs = self.collection.find({"album": name, "albumartist": artist})
        return convert_many(songs)

    def find_songs_by_folder(self, query: str) -> list:
        """
        Returns a sorted list of all the tracks exactly matching the folder in the query params
        """
        songs = self.collection.find({"folder": query}).sort(
            "title", db.pymongo.ASCENDING)
        return convert_many(songs)

    def find_songs_by_folder_og(self, query: str) -> list:
        """
        Returns an unsorted list of all the tracks exactly matching the folder in the query params
        """
        songs = self.collection.find({"folder": query})
        return convert_many(songs)

    def find_songs_by_artist(self, query: str) -> list:
        """
        Returns a list of all the tracks exactly matching the artists in the query params.
        """
        songs = self.collection.find({"artists": query})
        return convert_many(songs)

    def find_songs_by_albumartist(self, query: str):
        """
        Returns a list of all the tracks containing the albumartist in the query params.
        """
        songs = self.collection.find(
            {"albumartist": {"$regex": query, "$options": "i"}}
        )
        return convert_many(songs)

    def get_song_by_path(self, path: str) -> dict:
        """
        Returns a single track matching the filepath in the query params.
        """
        song = self.collection.find_one({"filepath": path})
        return convert_one(song)

    def remove_song_by_filepath(self, filepath: str):
        """
        Removes a single track from the database. Returns a boolean indicating success or failure of the operation.
        """
        try:
            self.collection.delete_one({"filepath": filepath})
            return True
        except:
            return False

    def remove_song_by_id(self, id: str):
        """
        Removes a single track from the database. Returns a boolean indicating success or failure of the operation.
        """
        try:
            self.collection.delete_one({"_id": ObjectId(id)})
            return True
        except:
            return False
