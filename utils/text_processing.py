from typing import List, Dict
import re

def text_processing(message: str, parts: List[Dict]) -> str:
    transformed_message = message

    for part in parts:
        part_payload = part["payload"]

        escaped_item = re.escape(part_payload["userId"])
        pattern = fr"@\[{escaped_item}\]"

        name = f"{part_payload.get("lastName", "")} {part_payload["firstName"]}".strip()

        transformed_message = re.sub(pattern, name, transformed_message)

    return transformed_message
