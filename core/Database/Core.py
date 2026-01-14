from pymongo import MongoClient
from core.files import Data

client = MongoClient(Data("config").json_read()["mongo"])

class Database:
    def __init__(self, dbName=None, colName=None):
        if not dbName or not colName:
            raise ValueError()
        
        self.db = client[dbName]
        self.col = self.db[colName]
    
    def get(self, **filter):
        return [doc for doc in self.col.find(filter)]
    
    def get_one(self, **filter):
        return self.col.find_one(filter)

    def drop(self):
        return self.col.drop()