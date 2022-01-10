import pymongo
import json
from bson import ObjectId, json_util


def convert_one_to_json(song):
    json_song = json.dumps(song, default=json_util.default)
    loaded_song = json.loads(json_song)

    return loaded_song


def convert_to_json(array):
    songs = []

    for song in array:
        json_song = json.dumps(song, default=json_util.default)
        loaded_song = json.loads(json_song)

        songs.append(loaded_song)

    return songs


class Mongo:
    def __init__(self, database):
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]


class Artists(Mongo):
    def __init__(self):
        super(Artists, self).__init__('ALL_ARTISTS')
        self.collection = self.db['THEM_ARTISTS']

    def insert_artist(self, artist_obj):
        self.collection.update_one(
            artist_obj, {'$set': artist_obj}, upsert=True)

    def get_all_artists(self):
        return self.collection.find()

    def get_artist_by_id(self, artist_id):
        return self.collection.find_one({'_id': ObjectId(artist_id)})

    def get_artists_by_name(self, query):
        return self.collection.find({'name': query}).limit(20)


class AllSongs(Mongo):
    def __init__(self):
        super(AllSongs, self).__init__('ALL_SONGS')
        self.collection = self.db['ALL_SONGS']

    # def drop_db(self):
    #     self.collection.drop()

    def insert_song(self, song_obj):
        self.collection.update_one(
            {'filepath': song_obj['filepath']}, {"$set": song_obj}, upsert=True)

    def get_all_songs(self):
        return convert_to_json(self.collection.find())

    def get_song_by_id(self, file_id):
        song = self.collection.find_one({'_id': ObjectId(file_id)})
        return convert_one_to_json(song)

    def get_song_by_album(self, name, artist):
        song = self.collection.find_one(
            {'album': name, 'album_artist': artist})
        return convert_one_to_json(song)

    def search_songs_by_album(self, query):
        songs = self.collection.find(
            {'album': {'$regex': query, '$options': 'i'}})
        return convert_to_json(songs)

    def search_songs_by_artist(self, query):
        songs = self.collection.find(
            {'artists': {'$regex': query, '$options': 'i'}})
        return convert_to_json(songs)

    def find_song_by_title(self, query):
        self.collection.create_index([('title', pymongo.TEXT)])
        song = self.collection.find(
            {'title': {'$regex': query, '$options': 'i'}})
        return convert_to_json(song)

    def find_songs_by_album(self, name, artist):
        songs = self.collection.find({'album': name, 'album_artist': artist})
        return convert_to_json(songs)

    def find_songs_by_folder(self, query):
        songs = self.collection.find({'folder': query}).sort(
            'title', pymongo.ASCENDING)
        return convert_to_json(songs)

    def find_songs_by_folder_og(self, query):
        songs = self.collection.find({'folder': query})
        return convert_to_json(songs)

    def find_songs_by_artist(self, query):
        songs = self.collection.find({'artists': query})
        return convert_to_json(songs)

    def find_songs_by_album_artist(self, query):
        songs = self.collection.find(
            {'album_artist': {'$regex': query, '$options': 'i'}})
        return convert_to_json(songs)

    def find_song_by_path(self, path):
        song = self.collection.find_one({'filepath': path})
        return convert_one_to_json(song)

    def remove_song_by_filepath(self, filepath):
        try:
            self.collection.remove({'filepath': filepath})
            return True
        except:
            return False
