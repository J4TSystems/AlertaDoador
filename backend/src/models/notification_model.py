from models.blood_stock_model import BloodType, StockStatus
from models.donor_model import Base
from sqlalchemy import Column, DateTime, Enum, String
from sqlalchemy.sql import func


class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(String, primary_key=True, index=True)
    recipient_email = Column(String, nullable=False)
    blood_type = Column(Enum(BloodType), nullable=False)
    status_at_time = Column(Enum(StockStatus), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
