from datetime import datetime
from pydantic import BaseModel

class Mention(BaseModel):
    id: int
    message_text: str
    mention_by: str
    mentioned: str
    datetime: datetime = datetime.now()