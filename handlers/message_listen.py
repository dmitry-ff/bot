from config import FLAG
import logging
logging.basicConfig(level=logging.INFO)
from utils import text_processing, check_same_user
from handlers import save_mention

def message_listen_cb(event, db):
    try:
        parts = event.data["parts"]

        if FLAG in event.text and parts and not check_same_user(event.data["from"]["userId"], parts):
            transformed_message = text_processing(event.text,parts)
            for part in parts:
                if part["type"] == "mention":
                    logging.info(f"Processing mention: {part}")
                    save_mention(event, part, db, transformed_message)
    except Exception as e:
        logging.error(f"Error in message_cb: {e}")