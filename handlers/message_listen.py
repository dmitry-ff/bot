from bot.bot import Bot

from config import FLAG, FILE
import logging
from utils import text_processing, get_mentions
from handlers.save_mention import save_mention
from utils import normalize_part, get_file_caption

def message_listen_cb(event, storage):
    try:
        corrected_parts = get_mentions(event.data["parts"]) if isinstance(event.text, str) else normalize_part(get_file_caption(event))
        corrected_text = event.text if isinstance(event.text, str) else get_file_caption(event)
        sender_id = event.data["from"]["userId"]

        if FLAG in corrected_text and corrected_parts:
            transformed_message = text_processing(corrected_text, corrected_parts)
            for part in corrected_parts:

                part_payload = part["payload"]
                if part_payload["userId"] != sender_id:
                    logging.info(f"Processing mention: {part_payload}")
                    save_mention(event, part, storage, transformed_message)
                    break
    except Exception as e:
        logging.error(f"Error in message_listen_cb: {e}")