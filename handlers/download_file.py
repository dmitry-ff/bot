import os
import logging
import pandas as pd
from utils import adjust_columns_width
from datetime import date

def download_file_cb(bot, event, mentions):
    excel_filename = f"Отчёт {date.today().strftime('%Y-%m-%d')}.xlsx"
    try:
        df = pd.DataFrame(mentions)
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

        df.to_excel(excel_filename, index=False)

        adjust_columns_width(excel_filename)

        with open(excel_filename, "rb") as file:
            bot.send_file(chat_id=event.from_chat, file=file)

    except Exception as e:
        logging.error(f"Error in download_file_cb: {e}")
    finally:
        os.remove(excel_filename)
