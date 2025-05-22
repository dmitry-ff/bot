import os

FLAG = "🍏"
PRIVATE_CHAT = "private"
GROUP_CHAT = "group"
MENTION = "mention"
ONBOARDING_PHRASE = "Привет! Данный бот умеет создавать отчёт, нажми кнопку, чтобы попробовать ⬇️"
DEFAULT_PHRASE = "Для создания отчёта нажми кнопку ⬇️"
NEW_FILE_PHRASE = "Для создания нового файла нажми кнопку ⬇️"
NO_ENTRIES_FOUND = f"На данный момент не было сохранено ни одного упоминания.\nЧтобы добавить запись, сделай следующее:\n\n1 - Перейди в чат, где подключен данный бот\n2 - Напиши какое то сообщение\n3 - Добавь флаг → {FLAG}\n4 - Добавь упоминание каких то людей\n\nP.S. Упоминание самого себя не будет сохранено"
START = "/start"

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGODB_URI=os.getenv("MONGODB_URI")
MONGODB_NAME=os.getenv("MONGODB_NAME")