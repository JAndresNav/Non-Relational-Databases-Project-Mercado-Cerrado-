from pymongo import MongoClient

def get_mongo_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["mercado_cerrado"]
