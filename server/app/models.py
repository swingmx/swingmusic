import pymongo
from bson import ObjectId


class Mongo:
    def __init__(self, database):
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]

class Artists(Mongo):
    def __init__(self):
        super(Artists, self).__init__('ALL_ARTISTS')
        self.collection = self.db['THEM_ARTISTS']

    def insert_artist(self, artist_obj):
        self.collection.update(artist_obj, artist_obj, upsert=True)

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

    def get_song_by_id(self, file_id):
        return self.collection.find_one({'_id': ObjectId(file_id)})

    def insert_song(self, song_obj):
        self.collection.update_one(
            {'filepath': song_obj['filepath']}, {"$set": song_obj}, upsert=True)

    def find_song_by_title(self, query):
        self.collection.create_index([('title', pymongo.TEXT)])
        return self.collection.find({'title': {'$regex': query, '$options': 'i'}})

    def find_songs_by_album(self, query):
        return self.collection.find({'album': {'$regex': query, '$options': 'i'}})

    def get_all_songs(self):
        return self.collection.find()

    def find_songs_by_folder(self, query, last_id=None):
        limit = 18
        if last_id is None:
            return self.collection.find({'folder': query}).limit(limit)
        else:
            return self.collection.find({'folder': query, '_id': {'$gt': ObjectId(last_id)}}).limit(limit)

    def find_songs_by_folder_og(self, query):
        return self.collection.find({'folder': query})

    def find_songs_by_artist(self, query):
        return self.collection.find({'artists': {'$regex': query, '$options': 'i'}})

    def find_songs_by_album_artist(self, query):
        return self.collection.find({'album_artist': {'$regex': query, '$options': 'i'}})

    def find_song_by_path(self, path):
        return self.collection.find_one({'filepath': path})

    def remove_song_by_filepath(self, filepath):
        try:
            self.collection.remove({'filepath': filepath})
            return True
        except:
            return False
