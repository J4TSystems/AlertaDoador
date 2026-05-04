from abc import ABC, abstractmethod


class EmailProvider(ABC):
    @abstractmethod
    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        pass
