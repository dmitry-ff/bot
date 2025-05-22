from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save_mention(self, mention_data: dict):
        pass

    @abstractmethod
    def get_mentions(self):
        pass

    @abstractmethod
    def get_mentions_by_msg_id(self, msg_id: str):
        pass

    @abstractmethod
    def update_message(self, message: str, msg_id: str, mentioned_id: str):
        pass

    @abstractmethod
    def get_mention_by_msg_id(self, msg_id: str):
        pass

    @abstractmethod
    def delete_mention(self, msg_id: str, mentioned_id: str):
        pass

    @abstractmethod
    def delete_mentions(self, msg_id: str):
        pass

    @abstractmethod
    def check_permission(self,  user_id: str):
        pass

    @abstractmethod
    def add_allowed_user(self,  user_id: str):
        pass