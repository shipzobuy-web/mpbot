from pymongo import MongoClient
from core.config import Config

# Use the environment variable from Config
client = MongoClient(Config.MONGO)

class Database:
    def __init__(self, dbName=None, colName=None):
        if not dbName or not colName:
            raise ValueError("Both dbName and colName must be provided")
        
        self.db = client[dbName]
        self.col = self.db[colName]
    
    def get(self, **filter):
        return [doc for doc in self.col.find(filter)]
    
    def get_one(self, **filter):
        return self.col.find_one(filter)

    def drop(self):
        return self.col.drop()
