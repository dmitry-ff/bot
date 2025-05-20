from config import MENTION

def get_mentions(parts):
    return [item for item in parts if item.get("type") == MENTION] if parts else []