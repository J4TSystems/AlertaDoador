from typing import List

from config.database import get_db
from config.settings import settings
from dtos.notification_dto import NotificationLogDTO
from email_infra.providers.mailpit_provider import MailpitProvider
from fastapi import APIRouter, Depends, status
from repositories.donor_repository import DonorRepository
from repositories.notification_repository import NotificationRepository
from repositories.stock_repository import StockRepository
from services.notification_service import NotificationService
from sqlalchemy.orm import Session

"""
    Orchestrates alerts by matching critical stocks with donors
    and managing dispatch history.
"""
router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    repository = NotificationRepository(db)
    stock_repository = StockRepository(db)
    donor_repository = DonorRepository(db)
    email_provider = MailpitProvider(host=settings.SMTP_HOST, port=settings.SMTP_PORT)
    return NotificationService(
        repository, stock_repository, donor_repository, email_provider
    )


@router.post(
    "/send-alerts",
    response_model=List[NotificationLogDTO],
    status_code=status.HTTP_200_OK,
)
def trigger_notifications(
    service: NotificationService = Depends(get_notification_service),
):
    return service.process_critical_notifications()


@router.get("/history", response_model=List[NotificationLogDTO])
def get_history(service: NotificationService = Depends(get_notification_service)):
    return service.get_sent_logs()
