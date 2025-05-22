from pymongo import MongoClient
import logging
from dotenv import load_dotenv
import os
from interfaces.storage import Storage

from utils.decorators import handle_mongo_errors

load_dotenv()

logger = logging.getLogger(__name__)

class MongoDB(Storage):
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

    def close(self):
        self.client.close()
        logger.info("MongoDB connection closed")

    @handle_mongo_errors
    def save_mention(self, mention_data: dict):
        result = self.mentions.insert_one(mention_data)
        logger.info(f"Inserted document with id: {result.inserted_id}")
        return result

    @handle_mongo_errors
    def get_mentions(self):
        cursor = self.mentions.find({}, {"_id": 0})
        result = list(cursor)
        logger.info(f"Fetched {len(result)} documents")
        return result

    @handle_mongo_errors
    def get_mentions_by_msg_id(self, msg_id):
        cursor = self.mentions.find({"msg_id": msg_id}, {"_id": 0})
        result = list(cursor)
        logger.info(f"Fetched {len(result)} documents with msg_id: {msg_id}")
        return result

    @handle_mongo_errors
    def update_message(self, message, msg_id, mentioned_id):
        self.mentions.update_one({"msg_id": msg_id, "mentioned_id": mentioned_id},
                                          {"$set": {"message_text": message}})
        logger.info(f"Updated message for mentioned id: {mentioned_id}")

    @handle_mongo_errors
    def get_mention_by_msg_id(self, msg_id):
        cursor = self.mentions.find_one({"msg_id": msg_id}, {"_id": 0})
        result = list(cursor)
        logger.info(f"Fetched {len(result)} documents with msg_id: {msg_id}")
        return result

    @handle_mongo_errors
    def delete_mention(self, msg_id, mentioned_id):
        result =  self.mentions.delete_one({"msg_id": msg_id, "mentioned_id": mentioned_id})
        logger.info(f"Deleted message for mentioned id: {mentioned_id}")
        return result.raw_result

    @handle_mongo_errors
    def delete_mentions(self, msg_id):
        result = self.mentions.delete_many({"msg_id": msg_id})
        logger.info(f"Deleted {result.deleted_count} documents with msg_id: {msg_id}")
        return result.deleted_count