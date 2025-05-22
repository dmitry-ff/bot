from bot.bot import Bot
import json

def send_keyboard(_bot: Bot, event, text):
    _bot.send_text(chat_id=event.from_chat,
                   text=text,
                   inline_keyboard_markup="{}".format(json.dumps([[
          {"text": "Создать отчёт", "callbackData": "call_back_id_1", "style": "primary"}
      ]])))