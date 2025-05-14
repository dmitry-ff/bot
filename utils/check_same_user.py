from typing import List, Dict

def check_same_user(mention_by: str, parts: List[Dict]) -> bool:
    return len(parts) == 1 and parts[0]["payload"]["userId"] == mention_by
