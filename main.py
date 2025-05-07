from bot.bot import Bot
from bot.handler import MessageHandler
from config import TOKEN, FLAG, GROUP_CHAT, PRIVATE_CHAT

from database.mongo import MongoDB

db = MongoDB()
bot = Bot(token=TOKEN)

def message_cb(bot, event):
    if event.data["chat"]["type"] == GROUP_CHAT:
        if FLAG in event.text:
            if event.data["parts"]:
                for part in event.data["parts"]:
                    if part["type"] == "mention":
                        print(part)
                        try:
                           db.save_mention(part)
                        except Exception as e: print(e)

    if event.data["chat"]["type"] == PRIVATE_CHAT:
        bot.send_message(event.data["chat"]["id"], event.data["text"])

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()