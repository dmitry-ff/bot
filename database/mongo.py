from pymongo import MongoClient
from config import MONGODB_URI, DB_NAME
import logging

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )

            self.client.server_info()
            self.db = self.client[DB_NAME]
            self.mentions = self.db.mentions
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"MongoDB connection error: {e}")
            raise

    def save_mention(self, mention_data: dict):
        try:
            result = self.mentions.insert_one(mention_data)
            logging.info(f"Inserted document with id: {result.inserted_id}")
            return result
        except Exception as e:
            logging.error(f"Error saving mention: {e}")
            raise
    def get_mentions(self):
        try:
            result = self.mentions.find({}, {"_id": 0})
            logging.info(f"Getting collection: {result}")
            return result
        except Exception as e:
            logging.error(f"Error getting mentions: {e}")
            raise
