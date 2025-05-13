import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = "001.0852096893.0629123419:1011881519" #your token here
FLAG = "#🍏"

PRIVATE_CHAT = "private"
GROUP_CHAT = "group"

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "gratitude"
