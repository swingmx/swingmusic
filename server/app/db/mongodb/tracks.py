"""
This file contains the AllSongs class for interacting with track documents in MongoDB.
"""
import re

import pymongo
from app.db.mongodb import convert_many
from app.db.mongodb import convert_one
from app.db.mongodb import MongoTracks
from bson import ObjectId


class Tracks(MongoTracks):
    """
    The class for all track-related database operations.
    """

    # def drop_db(self):
    #     self.collection.drop()

    def insert_song(self, song_obj: dict) -> str:
        """
        Inserts a new track object into the database.
        """
        return self.collection.update_one({
            "filepath": song_obj["filepath"]
        }, {
            "$set": song_obj
        },
                                          upsert=True).upserted_id

    def insert_many(self, songs: list):
        """
        Inserts multiple songs into the database.
        """
        return self.collection.insert_many(songs)

    def get_all_tracks(self) -> list:
        """
        Returns all tracks in the database.
        """
        return convert_many(self.collection.find())

    def get_track_by_id(self, id: str) -> dict:
        """
        Returns a track object by its mongodb id.
        """
        song = self.collection.find_one({"_id": ObjectId(id)})
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
            {"album": {
                "$regex": query,
                "$options": "i"
            }})
        return convert_many(songs)

    def search_songs_by_artist(self, query: str) -> list:
        """
        Returns all the songs matching the artists in the query params.
        """
        songs = self.collection.find(
            {"artists": {
                "$regex": query,
                "$options": "i"
            }})
        return convert_many(songs)

    def find_song_by_title(self, query: str) -> list:
        """
        Finds all the tracks matching the title in the query params.
        """
        song = self.collection.find(
            {"title": {
                "$regex": query,
                "$options": "i"
            }})
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
        songs = self.collection.find({
            "folder": query
        }).sort("title", pymongo.ASCENDING)
        return convert_many(songs)

    def find_songs_by_filenames(self, filenames: list) -> list:
        """
        Returns a list of all the tracks matching the filenames in the query params.
        """
        songs = self.collection.find({"filepath": {"$in": filenames}})
        return convert_many(songs)

    def find_songs_by_folder_og(self, query: str) -> list:
        """
        Returns an unsorted list of all the track matching the folder in the query params
        """
        songs = self.collection.find({"folder": query})
        return convert_many(songs)

    def get_dir_t_count(self, path: str) -> int:
        """
        Returns a list of all the tracks matching the path in the query params.
        """
        regex = re.compile(r"^.*" + re.escape(path) + r".*$")

        return self.collection.count_documents({"filepath": {"$regex": regex}})

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
            {"albumartist": {
                "$regex": query,
                "$options": "i"
            }})
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

    def find_tracks_by_hash(self, hash: str) -> list:
        """
        Returns a list of all the tracks matching the hash in the query params.
        """
        songs = self.collection.find({"albumhash": hash})
        return convert_many(songs)

    def find_track_by_title_artists_album(self, title: str, artist: str,
                                          album: str) -> dict:
        """
        Returns a single track matching the title, artist, and album in the query params.
        """
        song = self.collection.find_one({
            "title": title,
            "artists": artist,
            "album": album
        })
        return convert_one(song)
