from config import MENTION, FILE

def get_mentions(parts):
    return [item for item in parts if item.get("type") == MENTION or item.get("type") == FILE] if parts else []