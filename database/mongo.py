from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.mentions = self.db.mention

    def save_mention(self, mention_data: dict):
        print(mention_data)
        return self.mentions.insert_one(mention_data)