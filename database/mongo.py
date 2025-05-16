from pymongo import MongoClient
import logging
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient(
                os.getenv("MONGODB_URI"),
                serverSelectionTimeoutMS=5000
            )

            self.client.server_info()
            self.db = self.client[os.getenv("MONGODB_NAME")]
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

    def get_mentions_by_msg_id(self, msg_id):
        try:
            result = self.mentions.find({"msgId": msg_id}, {"_id": 0})
            return result
        except Exception as e:
            logging.error(f"Error getting mentions by msg id: {e}")
            raise
    def update_message(self, message, msg_id):
        try:
            result = self.mentions.update_many({"msgId": msg_id}, {"$set": {"message_text": message}})
            logging.info(f"Documents updated count: {result}")
        except Exception as e:
            logging.error(f"Error while updating mentions: {e}")
            raise
    def get_mention(self, mentioned_id, msg_id):
        try:
            return self.mentions.find_one({"mentioned_id": mentioned_id, "msgId": msg_id}, {"_id": 0})
        except Exception as e:
            logging.error(f"Error while getting mention: {e}")
            raise
    def get_mention_by_msg_id(self, msg_id):
        try:
            return self.mentions.find_one({"msgId": msg_id}, {"_id": 0})
        except Exception as e:
            logging.error(f"Error while getting mention: {e}")
            raise
    def delete_mentions(self, msg_id):
        try:
            return self.mentions.delete_many({"msgId": msg_id})
        except Exception as e:
            logging.error(f"Error while deleting mentions: {e}")
            raise