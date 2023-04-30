from pymongo import MongoClient


def get_db(db_name):
    client = MongoClient(host="0.0.0.0", port=27017)
    db = client[db_name]
    return db

def get_db_collection(db_name, db_collection):
    client = MongoClient(host="0.0.0.0", port=27017)
    db = client[db_name]
    collection = db[db_collection]
    return collection


