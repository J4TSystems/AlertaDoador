from datetime import datetime

from models.blood_stock_model import BloodType, StockStatus
from pydantic import BaseModel


class NotificationLogDTO(BaseModel):
    id: str
    recipient_email: str
    blood_type: BloodType
    status_at_time: StockStatus
    sent_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    message: str
