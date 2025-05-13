from bot.bot import Bot
from bot.handler import MessageHandler
import os
from config import TOKEN, FLAG, GROUP_CHAT, PRIVATE_CHAT
import logging
logging.basicConfig(level=logging.INFO)
from datetime import date
import pandas as pd
from openpyxl import load_workbook
import re

from database.mongo import MongoDB

db = MongoDB()
bot = Bot(token=TOKEN)

def transform_ids_to_names(message, parts):
    transformed_message = message

    for part in parts:
        part_payload = part["payload"]

        escaped_item = re.escape(part_payload["userId"])
        pattern = fr"@\[{escaped_item}\]"

        name = f"{part_payload.get("lastName", "")} {part_payload["firstName"]}".strip()

        transformed_message = re.sub(pattern, name, transformed_message)

    return transformed_message

def adjust_columns_width(file_name):
    wb = load_workbook(file_name)

    ws = wb.active

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass

        ws.column_dimensions[column_letter].width = max_length + 2

    wb.save(file_name)

def download_file_cb(bot, event):
    try:
        data = list(db.get_mentions())
        df = pd.DataFrame(data)
        desired_columns = ["message_text", "mention_by", "mention_by_id", "mentioned", "mentioned_id", "datetime"]

        df = df[desired_columns]
        df = df.rename(columns={
            "message_text": "Сообщение",
            "mention_by": "Отправитель",
            "mention_by_id": "ID отправителя",
            "mentioned": "Кого упомянули",
            "mentioned_id": "ID упомянутого",
            "datetime": "Дата",
        })
        df.drop("_id", axis=1, inplace=True, errors="ignore")

        excel_filename = "Отчёт.xlsx"
        df.to_excel(excel_filename, index=False)

        adjust_columns_width(excel_filename)

        with open(excel_filename, "rb") as file:
            bot.send_file(chat_id=event.from_chat, file=file)

        os.remove(excel_filename)
    except Exception as e:
        logging.error(f"Error in message_cb: {e}")

def message_listen_cb(event):
    try:
        if FLAG in event.text and event.data["parts"]:
            transformed_message = transform_ids_to_names(event.text, event.data["parts"])

            print(transformed_message)
            for part in event.data["parts"]:
                if part["type"] == "mention":
                    logging.info(f"Processing mention: {part}")
                    print(part)
                    today = date.today().strftime('%Y-%m-%d')
                    mention_by = event.data["from"]
                    mentioned = part["payload"]
                    last_name = mentioned.get("lastName", "")

                    mention_data = {
                        "message_text": transformed_message,
                        "mention_by": f"{mention_by["lastName"]} {mention_by["firstName"]}",
                        "mention_by_id": mention_by["userId"],
                        "mentioned": f"{mentioned['firstName']} {last_name}".strip(),
                        "mentioned_id": mentioned["userId"],
                        "datetime": today
                    }
                    db.save_mention(mention_data)
    except Exception as e:
        logging.error(f"Error in message_cb: {e}")

def message_cb(bot, event):
    chat_type = event.data["chat"]["type"]

    if chat_type == GROUP_CHAT:
        message_listen_cb(event)

    if chat_type == PRIVATE_CHAT:
        download_file_cb(bot, event)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()