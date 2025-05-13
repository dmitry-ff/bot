from config import FLAG
import logging
logging.basicConfig(level=logging.INFO)
from datetime import date
from utils.text_processing import text_processing

def message_listen_cb(event, db):
    try:
        if FLAG in event.text and event.data["parts"]:
            transformed_message = text_processing(event.text, event.data["parts"])

            print(transformed_message)
            for part in event.data["parts"]:
                if part["type"] == "mention":
                    logging.info(f"Processing mention: {part}")
                    print(part)
                    today = date.today().strftime('%Y-%m-%d')
                    mention_by = event.data["from"]
                    mentioned = part["payload"]
                    last_name = mentioned.get("lastName", "")

                    mention_data = {
                        "message_text": transformed_message,
                        "mention_by": f"{mention_by["lastName"]} {mention_by["firstName"]}",
                        "mention_by_id": mention_by["userId"],
                        "mentioned": f"{mentioned['firstName']} {last_name}".strip(),
                        "mentioned_id": mentioned["userId"],
                        "datetime": today
                    }
                    db.save_mention(mention_data)
    except Exception as e:
        logging.error(f"Error in message_cb: {e}")