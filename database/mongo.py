from pymongo import MongoClient
import logging
from interfaces.storage import Storage
from config import MONGODB_URI, MONGODB_NAME

from utils import handle_mongo_errors


logger = logging.getLogger(__name__)

class MongoDB(Storage):
    def __init__(self):
        try:
            self.client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )

            self.client.server_info()
            self.db = self.client[MONGODB_NAME]

            self._init_collections()

            self.mentions = self.db.mentions
            self.access = self.db.access
            logging.info("Successfully connected to MongoDB")
        except Exception as e:
            logging.error(f"MongoDB connection error: {e}")
            raise

    def _init_collections(self):
        if "access" not in self.db.list_collection_names():
            self.db.access.insert_many([
                {"user_id": "kozlov@ddplanet.ru"},
                {"user_id": "stepina@ddplanet.ru"},
                {"user_id": "matrenin@ddplanet.ru"},
                {"user_id": "polosina@ddplanet.ru"},
                {"user_id": "zibina@ddplanet.ru"},

            ])
            logger.info("Created 'access' collection with default users")

        if "mentions" not in self.db.list_collection_names():
            self.db.create_collection("mentions")
            logger.info("Created empty 'mentions' collection")

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
        cursor = self.mentions.find({"msg_id": msg_id}, {"_id": 0})
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

    @handle_mongo_errors
    def check_permission(self, user_id):
        result = self.access.find_one({"user_id": user_id}, {"_id": 0})
        return True if result else False

    @handle_mongo_errors
    def add_allowed_user(self, user_id):
        self.access.insert_one({"user_id": user_id})
        logger.info(f"Added allowed user {user_id}")

