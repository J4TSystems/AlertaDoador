from typing import Dict, List

from dtos.notification_dto import NotificationLogDTO
from repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    def process_critical_notifications(self) -> Dict[str, str]:
        """
        Return a simple dictionary message.
        """
        return {"message": "Alerts processed. 0 emails sent."}

    def get_sent_logs(self) -> List[NotificationLogDTO]:
        """
        Return an empty list [].
        """
        return []
