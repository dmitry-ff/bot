import re
from config import MENTION_REGEXP, MENTION


def normalize_part(caption):
    mentions = re.findall(MENTION_REGEXP, caption)

    return [{"payload": {"firstName": mention, "lastName": "", "userId": mention}, "type": MENTION} for mention in mentions]