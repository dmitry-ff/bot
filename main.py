from bot.bot import Bot
from bot.handler import MessageHandler, DeletedMessageHandler, EditedMessageHandler

from config import GROUP_CHAT, PRIVATE_CHAT
import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
import os
from handlers import  download_file_cb, message_listen_cb, save_mention
from database.mongo import MongoDB
from utils import  text_processing
from config import FLAG

load_dotenv()

db = MongoDB()
bot = Bot(token=os.getenv("BOT_TOKEN"))

def new_message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        message_listen_cb(event, db)

    if chat_type == PRIVATE_CHAT:
        data = list(db.get_mentions())
        download_file_cb(bot, event, data)

def delete_message_cb(bot, event):
    print(bot, event)


def edit_message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        parts = event.data["parts"]
        message = event.data["text"]
        transformed_data = text_processing(event.data["text"], parts)
        mentions_by_msg_id = db.get_mentions_by_msg_id(event.data["msgId"])

        #удалит все сообщения, если при редактировании флаг был удалён
        if FLAG not in message:
            db.delete_mentions(event.data["msgId"])
            return

        #добавит записи на каждого упомянутого, если к сообщению был добавлен флаг
        if FLAG in message and not db.get_mention_by_msg_id(event.data["msgId"]):
            for part in event.data["parts"]:
                save_mention(event, part, db, transformed_data)
            return

        #Удалит запись, если во входящем сообщении нет упоминания о человеке, сохраненном с данным msgId, обновит существующие
        if len(list(mentions_by_msg_id)) > len(parts):
            print(parts)
            for mention in mentions_by_msg_id:
                for part in parts:
                    part["userId"] == mention["mention_id"]
            return

        #Добавит запись на каждого нового упомянутого человека и обновит сообщения для уже существующих
        if len(list(mentions_by_msg_id)) < len(parts):
            for part in event.data["parts"]:
                payload = part["payload"]
                msg_id = event.data["msgId"]
                mentioned_id = payload["userId"]

                if db.get_mention(mentioned_id, msg_id):
                    db.update_message(transformed_data, msg_id)
                else:
                    save_mention(event, part, db, transformed_data)
            return

bot.dispatcher.add_handler(DeletedMessageHandler(callback=delete_message_cb))
bot.dispatcher.add_handler(EditedMessageHandler(callback=edit_message_cb))
bot.dispatcher.add_handler(MessageHandler(callback=new_message_cb))


bot.start_polling()
bot.idle()