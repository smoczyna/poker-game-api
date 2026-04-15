import gridfs
import pymongo

__author__ = 'smok'

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    URI_AUTH = "mongodb://pokermaster:pokermaster@localhost:27017/pokergame?authSource=pokergame"
    DB_NAME = 'pokergame'
    DATABASE = None

    @staticmethod
    def get_db(collection):
        return Database.DATABASE[collection]

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI_AUTH)
        Database.DATABASE = client[Database.DB_NAME]
        print('Connected to: ' + Database.DATABASE.name)

    @staticmethod
    def get_db_fs():
        if Database.DATABASE is None:
            Database.initialize()
        return gridfs.GridFS(Database.DATABASE, "files")

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        if Database.DATABASE is None:
            Database.initialize()

        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        if Database.DATABASE is None:
            Database.initialize()

        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_aggr(collection, query, predict):
        if Database.DATABASE is None:
            Database.initialize()

        return Database.DATABASE[collection].find(query, predict)

    @staticmethod
    def count(collection, query):
        if Database.DATABASE is None:
            Database.initialize()

        return Database.DATABASE[collection].count_documents(query)

    @staticmethod
    def update(collection, query, payload):
        return Database.DATABASE[collection].update_one(query, {"$set": payload})

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].delete_one(query)

    @staticmethod
    def insert_many(collection, data):
        Database.DATABASE[collection].insert_many(data)
