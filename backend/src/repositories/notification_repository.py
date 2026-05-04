from typing import List

from models.notification_model import NotificationLog
from sqlalchemy import desc
from sqlalchemy.orm import Session


class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[NotificationLog]:
        return (
            self.db.query(NotificationLog).order_by(desc(NotificationLog.sent_at)).all()
        )

    def save(self, notification: NotificationLog) -> NotificationLog:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
