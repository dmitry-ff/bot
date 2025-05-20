import logging
logging.basicConfig(level=logging.INFO)
from handlers import  save_mention
from utils import  text_processing, get_mentions
from config import FLAG

def edit_message(event, db):
    msg_id = event.data["msgId"]
    # обработать кейс, когда на вход even.data.get("parts") пусто
    mentions_from_event = get_mentions(event.data.get("parts"))
    message = event.data["text"]
    transformed_data = text_processing(event.data["text"], mentions_from_event)
    mentions_by_msg_id = list(db.get_mentions_by_msg_id(msg_id))

    # удалит все сообщения, если при редактировании флаг был удалён
    if FLAG not in message:
        db.delete_mentions(msg_id)
        return

    # добавит записи на каждого упомянутого, если к сообщению был добавлен флаг
    if FLAG in message and not db.get_mention_by_msg_id(msg_id):
        for part in event.data["parts"]:
            save_mention(event, part, db, transformed_data)
        return

    db_dict = {(obj['mentioned_id']): obj for obj in mentions_by_msg_id}
    api_dict = {(obj["payload"]['userId']): obj for obj in mentions_from_event}

    to_delete = [(db_dict[k]) for k in db_dict if k not in api_dict]
    to_create = [(api_dict[k]) for k in api_dict if k not in db_dict]
    to_update = [(api_dict[k]) for k in api_dict if k in db_dict]

    for obj in to_delete:
        db.delete_mention(msg_id, obj["mentioned_id"])

    for obj in to_create:
        save_mention(event, obj, db, transformed_data)

    for obj in to_update:
        db.update_message(transformed_data, msg_id, obj["payload"]["userId"])
