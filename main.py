from bot.bot import Bot
from bot.handler import MessageHandler, DeletedMessageHandler, EditedMessageHandler, StartCommandHandler, BotButtonCommandHandler
import atexit
from config import GROUP_CHAT, PRIVATE_CHAT, ONBOARDING_PHRASE, DEFAULT_PHRASE, START
import logging
from dotenv import load_dotenv
import os
from handlers import  message_listen_cb, edit_message, buttons_answer_cb
from database.mongo import MongoDB
from utils import send_keyboard, not_allowed

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = MongoDB()
atexit.register(db.close)

bot = Bot(token=os.getenv("BOT_TOKEN"))

def start_cb(_bot: Bot, event):
    if db.check_permission(event.data["from"]["userId"]):
        send_keyboard(_bot=_bot, event=event, text=ONBOARDING_PHRASE)
    else:
        not_allowed(_bot, event)

def new_message_cb(_bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT and event.data.get("parts"):
        message_listen_cb(event, db)
        return

    if chat_type == PRIVATE_CHAT and event.text != START and not db.check_permission(event.data["from"]["userId"]):
        not_allowed(_bot, event)
        return

    if chat_type == PRIVATE_CHAT and event.text != START and db.check_permission(event.data["from"]["userId"]):
        send_keyboard(_bot=_bot, event=event, text=DEFAULT_PHRASE)
        return

#TODO: изучить, как работает хендлер для получения эвента удаления сообщения
def delete_message_cb(_bot, event):
    print(_bot, event)


def edit_message_cb(_, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        edit_message(event, db)

bot.dispatcher.add_handler(StartCommandHandler(callback=lambda bot, event: start_cb(_bot=bot, event=event)))
bot.dispatcher.add_handler(DeletedMessageHandler(callback=lambda bot: delete_message_cb(_bot=bot)))
bot.dispatcher.add_handler(EditedMessageHandler(callback=edit_message_cb))
bot.dispatcher.add_handler(MessageHandler(callback=lambda bot, event: new_message_cb(_bot=bot, event=event)))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=lambda bot, event: buttons_answer_cb(bot, event, db)))

if __name__ == '__main__':
    try:
        logger.info("Starting bot polling")
        bot.start_polling()
        bot.idle()
    finally:
        db.close()