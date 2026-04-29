from typing import List

from config.database import get_db
from dtos.notification_dto import NotificationLogDTO
from fastapi import APIRouter, Depends, status
from repositories.notification_repository import NotificationRepository
from services.notification_service import NotificationService
from sqlalchemy.orm import Session

"""
    Orchestrates alerts by matching critical stocks with donors
    and managing dispatch history.
"""
router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    repository = NotificationRepository(db)
    return NotificationService(repository)


@router.post("/send-alerts", status_code=status.HTTP_200_OK)
def trigger_notifications(
    service: NotificationService = Depends(get_notification_service),
):
    return service.process_critical_notifications()


@router.get("/history", response_model=List[NotificationLogDTO])
def get_history(service: NotificationService = Depends(get_notification_service)):
    return service.get_sent_logs()
