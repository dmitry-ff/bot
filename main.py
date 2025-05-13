from bot.bot import Bot
from bot.handler import MessageHandler
from config import GROUP_CHAT, PRIVATE_CHAT
import logging
logging.basicConfig(level=logging.INFO)
from dotenv import load_dotenv
import os


from handlers.download_file import  download_file_cb
from handlers.message_listen import message_listen_cb

from database.mongo import MongoDB

load_dotenv()

db = MongoDB()
bot = Bot(token=os.getenv("BOT_TOKEN"))

def message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        message_listen_cb(event, db)

    if chat_type == PRIVATE_CHAT:
        data = list(db.get_mentions())
        download_file_cb(bot, event, data)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()