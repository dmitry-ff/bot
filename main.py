from bot.bot import Bot
import json
from bot.handler import MessageHandler, DeletedMessageHandler, EditedMessageHandler, StartCommandHandler, BotButtonCommandHandler
import atexit
from config import GROUP_CHAT, PRIVATE_CHAT, ONBOARDING_PHRASE, DEFAULT_PHRASE, START, NEW_FILE_PHRASE, \
    NO_ENTRIES_FOUND, DOWNLOAD_ACCESS
import logging
from dotenv import load_dotenv
import os
from handlers import  download_file_cb, message_listen_cb, edit_message
from database.mongo import MongoDB

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = MongoDB()
atexit.register(db.close)

bot = Bot(token=os.getenv("BOT_TOKEN"))

def send_keyboard(_bot: Bot, event, text):
    _bot.send_text(chat_id=event.from_chat,
                   text=text,
                   inline_keyboard_markup="{}".format(json.dumps([[
          {"text": "Создать отчёт", "callbackData": "call_back_id_1", "style": "primary"}
      ]])))

def buttons_answer_cb(bot: Bot, event):
    if event.data["callbackData"] == "call_back_id_1":
        data = db.get_mentions()
        if len(data) > 0:
            download_file_cb(bot, event=event, mentions=data)
            bot.answer_callback_query(
                query_id=event.data["queryId"],
                text="",
                show_alert=False,
            )
            send_keyboard(_bot=bot, event=event, text=NEW_FILE_PHRASE)
        else:
            print(event)
            bot.answer_callback_query(
                query_id=event.data["queryId"],
                text="",
                show_alert=False,
            )
            send_keyboard(_bot=bot, event=event, text=NO_ENTRIES_FOUND)


def start_cb(bot: Bot, event):
    if event.data["from"]["userId"] in DOWNLOAD_ACCESS:
        send_keyboard(_bot=bot, event=event, text=ONBOARDING_PHRASE)
    else:
        bot.send_text(chat_id=event.from_chat,
           text="❌ У вас нет доступа к этой функции.",
           )

def new_message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT and event.data.get("parts"):
        message_listen_cb(event, db)

    if chat_type == PRIVATE_CHAT and event.data["from"]["userId"] and event.text != START not in DOWNLOAD_ACCESS:
        bot.send_text(chat_id=event.from_chat,
                      text="❌ У вас нет доступа к этой функции.",
                      )

    if chat_type == PRIVATE_CHAT and event.text != START and event.data["from"]["userId"] in DOWNLOAD_ACCESS:
        send_keyboard(_bot=bot, event=event, text=DEFAULT_PHRASE)

#TODO: изучить, как работает хендлер для получения эвента удаления сообщения
def delete_message_cb(_bot, event):
    print(_bot, event)


def edit_message_cb(_, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        edit_message(event, db)

bot.dispatcher.add_handler(StartCommandHandler(callback=start_cb))
bot.dispatcher.add_handler(DeletedMessageHandler(callback=delete_message_cb))
bot.dispatcher.add_handler(EditedMessageHandler(callback=edit_message_cb))
bot.dispatcher.add_handler(MessageHandler(callback=new_message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

if __name__ == '__main__':
    try:
        logger.info("Starting bot polling")
        bot.start_polling()
        bot.idle()
    finally:
        db.close()