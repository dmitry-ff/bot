from bot.bot import Bot
from bot.handler import MessageHandler, DeletedMessageHandler, EditedMessageHandler

from config import GROUP_CHAT, PRIVATE_CHAT
import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
import os
from handlers import  download_file_cb, message_listen_cb, edit_message
from database.mongo import MongoDB

load_dotenv()

db = MongoDB()
bot = Bot(token=os.getenv("BOT_TOKEN"))

def new_message_cb(bot, event):
    chat_type = event.data["chat"]["type"]
    print(event)

    if chat_type == GROUP_CHAT and event.data.get("parts"):
        message_listen_cb(event, db)

    if chat_type == PRIVATE_CHAT:
        data = list(db.get_mentions())
        download_file_cb(bot, event, data)

def delete_message_cb(bot, event):
    print(bot, event)


def edit_message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        edit_message(event, db)


bot.dispatcher.add_handler(DeletedMessageHandler(callback=delete_message_cb))
bot.dispatcher.add_handler(EditedMessageHandler(callback=edit_message_cb))
bot.dispatcher.add_handler(MessageHandler(callback=new_message_cb))


bot.start_polling()
bot.idle()