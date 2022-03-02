import json
from dataclasses import dataclass
import pymongo
from bson import ObjectId, json_util


def convert_one_to_json(song):
    """
    Converts a single mongodb cursor to a json object.
    """
    json_song = json.dumps(song, default=json_util.default)
    loaded_song = json.loads(json_song)

    return loaded_song


def convert_to_json(array):
    """
    Converts a list of mongodb cursors to a list of json objects.
    """

    songs = []

    for song in array:
        json_song = json.dumps(song, default=json_util.default)
        loaded_song = json.loads(json_song)

        songs.append(loaded_song)

    return songs


class Mongo:
    """
    The base class for all mongodb classes.
    """

    def __init__(self, database):
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]


class Artists(Mongo):
    """
    The artist class for all artist related database operations.
    """

    def __init__(self):
        super(Artists, self).__init__("ALL_ARTISTS")
        self.collection = self.db["THEM_ARTISTS"]

    def insert_artist(self, artist_obj: dict) -> None:
        """
        Inserts an artist into the database.
        """
        self.collection.update_one(
            artist_obj, {"$set": artist_obj}, upsert=True
        ).upserted_id

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


class AllSongs(Mongo):
    """
    The class for all track-related database operations.
    """

    def __init__(self):
        super(AllSongs, self).__init__("ALL_SONGS")
        self.collection = self.db["ALL_SONGS"]

    # def drop_db(self):
    #     self.collection.drop()

    def insert_song(self, song_obj: dict) -> None:
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
        return convert_to_json(self.collection.find())

    def get_song_by_id(self, file_id: str) -> dict:
        """
        Returns a track object by its mongodb id.
        """
        song = self.collection.find_one({"_id": ObjectId(file_id)})
        return convert_one_to_json(song)

    def get_song_by_album(self, name: str, artist: str) -> dict:
        """
        Returns a single track matching the album in the query params.
        """
        song = self.collection.find_one({"album": name, "albumartist": artist})
        return convert_one_to_json(song)

    def search_songs_by_album(self, query: str) -> list:
        """
        Returns all the songs matching the albums in the query params (using regex).
        """
        songs = self.collection.find({"album": {"$regex": query, "$options": "i"}})
        return convert_to_json(songs)

    def search_songs_by_artist(self, query: str) -> list:
        """
        Returns all the songs matching the artists in the query params.
        """
        songs = self.collection.find({"artists": {"$regex": query, "$options": "i"}})
        return convert_to_json(songs)

    def find_song_by_title(self, query: str) -> list:
        """
        Finds all the tracks matching the title in the query params.
        """
        self.collection.create_index([("title", pymongo.TEXT)])
        song = self.collection.find({"title": {"$regex": query, "$options": "i"}})
        return convert_to_json(song)

    def find_songs_by_album(self, name: str, artist: str) -> list:
        """
        Returns all the tracks exactly matching the album in the query params.
        """
        songs = self.collection.find({"album": name, "albumartist": artist})
        return convert_to_json(songs)

    def find_songs_by_folder(self, query: str) -> list:
        """
        Returns a sorted list of all the tracks exactly matching the folder in the query params
        """
        songs = self.collection.find({"folder": query}).sort("title", pymongo.ASCENDING)
        return convert_to_json(songs)

    def find_songs_by_folder_og(self, query: str) -> list:
        """
        Returns an unsorted list of all the tracks exactly matching the folder in the query params
        """
        songs = self.collection.find({"folder": query})
        return convert_to_json(songs)

    def find_songs_by_artist(self, query: str) -> list:
        """
        Returns a list of all the tracks exactly matching the artists in the query params.
        """
        songs = self.collection.find({"artists": query})
        return convert_to_json(songs)

    def find_songs_by_albumartist(self, query: str):
        """
        Returns a list of all the tracks containing the albumartist in the query params.
        """
        songs = self.collection.find(
            {"albumartist": {"$regex": query, "$options": "i"}}
        )
        return convert_to_json(songs)

    def get_song_by_path(self, path: str) -> dict:
        """
        Returns a single track matching the filepath in the query params.
        """
        song = self.collection.find_one({"filepath": path})
        return convert_one_to_json(song)

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


class TrackColors(Mongo):
    """
    The class for all track-related database operations.
    """

    def __init__(self):
        super(TrackColors, self).__init__("TRACK_COLORS")
        self.collection = self.db["TRACK_COLORS"]

    def insert_track_color(self, track_color: dict) -> None:
        """
        Inserts a new track object into the database.
        """
        return self.collection.update_one(
            {"filepath": track_color["filepath"]},
            {"$set": track_color},
            upsert=True,
        ).upserted_id

    def get_track_color_by_track(self, filepath: str) -> dict:
        """
        Returns a track color object by its filepath.
        """
        track_color = self.collection.find_one({"filepath": filepath})
        return convert_one_to_json(track_color)


@dataclass
class Track:
    """
    Track class
    """

    trackid: str
    title: str
    artists: str
    albumartist: str
    album: str
    folder: str
    filepath: str
    length: int
    date: int
    genre: str
    bitrate: int
    image: str
    tracknumber: int
    discnumber: int

    def __init__(self, tags):
        self.trackid = tags["_id"]["$oid"]
        self.title = tags["title"]
        self.artists = tags["artists"].split(", ")
        self.albumartist = tags["albumartist"]
        self.album = tags["album"]
        self.folder = tags["folder"]
        self.filepath = tags["filepath"]
        self.length = tags["length"]
        self.date = tags["date"]
        self.genre = tags["genre"]
        self.bitrate = tags["bitrate"]
        self.image = "http://127.0.0.1:8900/images/thumbnails/" + tags["image"]
        self.tracknumber = tags["tracknumber"]
        self.discnumber = tags["discnumber"]
