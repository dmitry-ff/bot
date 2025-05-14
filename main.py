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

        transformed_data = text_processing(event.data["text"], parts)
        mentions_by_msg_id = db.get_mentions_by_msg_id(event.data["msgId"])


        if len(list(mentions_by_msg_id)) > len(parts):
            print(parts)
            for mention in mentions_by_msg_id:
                for part in parts:
                    part["userId"] == mention["mention_id"]

        if len(list(mentions_by_msg_id)) < len(parts):
            for part in event.data["parts"]:
                payload = part["payload"]
                msg_id = event.data["msgId"]
                mentioned_id = payload["userId"]

                if db.get_mention(mentioned_id, msg_id):
                    db.update_message(transformed_data, msg_id)
                else:
                    save_mention(event, part, db, transformed_data)

bot.dispatcher.add_handler(DeletedMessageHandler(callback=delete_message_cb))
bot.dispatcher.add_handler(EditedMessageHandler(callback=edit_message_cb))
bot.dispatcher.add_handler(MessageHandler(callback=new_message_cb))


bot.start_polling()
bot.idle()