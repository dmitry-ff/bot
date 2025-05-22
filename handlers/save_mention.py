from datetime import date

def save_mention(event, part, storage, message):
    mention_by = event.data["from"]
    mentioned = part["payload"]
    datetime = date.today().strftime('%Y-%m-%d')

    mention_data = {
        "message_text": message,
        "mention_by": f"{mention_by.get('lastName', '')} {mention_by.get('firstName', '')}".strip(),
        "mention_by_id": mention_by.get("userId"),
        "mentioned": f"{mentioned.get('firstName', '')} {mentioned.get('lastName', '')}".strip(),
        "mentioned_id": mentioned.get("userId"),
        "datetime": datetime,
        "msg_id": event.data.get("msgId")
    }

    storage.save_mention(mention_data)