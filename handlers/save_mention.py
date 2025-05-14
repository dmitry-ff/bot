from datetime import date

def save_mention(event, part, db, message):
    today = date.today().strftime('%Y-%m-%d')
    mention_by = event.data["from"]
    mentioned = part["payload"]
    last_name = mentioned.get("lastName", "")

    mention_data = {
        "message_text": message,
        "mention_by": f"{mention_by["lastName"]} {mention_by["firstName"]}",
        "mention_by_id": mention_by["userId"],
        "mentioned": f"{mentioned['firstName']} {last_name}".strip(),
        "mentioned_id": mentioned["userId"],
        "datetime": today,
        "msgId": event.data["msgId"]
    }
    db.save_mention(mention_data)