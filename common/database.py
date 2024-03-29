import pymongo
from typing import Dict, List
import os


class Database(object):
    # URI = "mongodb://127.0.0.1:27017/pricing"
    URI = os.getenv('MONGO_URI')
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def search(collection:str, search: str)->List[Dict]:
        return Database.DATABASE[collection].find({"$text": {"$search": search}})

    @staticmethod
    def get_random(collection:str, size:int):
        return Database.DATABASE[collection].aggregate([{ "$sample": { "size": size } }])

    @staticmethod
    def latest(collection:str)->Dict:
        return Database.DATABASE[collection].find({}).sort([("$natural",-1)]).limit(1)[0]