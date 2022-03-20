import pymongo
import json
from bson import json_util


class Mongo:
    """
    The base class for all mongodb classes.
    """

    def __init__(self, database):
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]


def convert_one(song):
    """
    Converts a single mongodb cursor to a json object.
    """
    json_song = json.dumps(song, default=json_util.default)
    loaded_song = json.loads(json_song)

    return loaded_song


def convert_many(array):
    """
    Converts a list of mongodb cursors to a list of json objects.
    """

    songs = []

    for song in array:
        json_song = json.dumps(song, default=json_util.default)
        loaded_song = json.loads(json_song)

        songs.append(loaded_song)

    return songs
