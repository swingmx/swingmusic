import pymongo

class Mongo:
    """
    The base class for all mongodb classes.
    """

    def __init__(self, database):
        mongo_uri = pymongo.MongoClient()
        self.db = mongo_uri[database]

class MongoAlbums(Mongo):
    def __init__(self):
        super(MongoAlbums, self).__init__("ALICE_ALBUMS")
        self.collection = self.db["ALL_ALBUMS"]