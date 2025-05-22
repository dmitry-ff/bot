from bot.bot import Bot
from config import  NEW_FILE_PHRASE, NO_ENTRIES_FOUND
from handlers import  download_file_cb, message_listen_cb, edit_message
from utils import send_keyboard

def buttons_answer_cb(bot: Bot, event, db):
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
