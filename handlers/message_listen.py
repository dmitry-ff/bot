from config import FLAG
import logging
from utils import text_processing, get_mentions
from handlers.save_mention import save_mention

def message_listen_cb(event, storage):
    try:
        parts = get_mentions(event.data["parts"])
        sender_id = event.data["from"]["userId"]

        if FLAG in event.text and parts:
            transformed_message = text_processing(event.text, parts)
            for part in parts:
                part_payload = part["payload"]
                if part_payload["userId"] != sender_id:
                    logging.info(f"Processing mention: {part_payload}")
                    save_mention(event, part, storage, transformed_message)
    except Exception as e:
        logging.error(f"Error in message_listen_cb: {e}")