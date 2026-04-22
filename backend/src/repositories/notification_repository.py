from typing import List

from models.notification_model import NotificationLog
from sqlalchemy.orm import Session


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[NotificationLog]:
        pass

    def save(self, notification: NotificationLog) -> NotificationLog:
        pass
