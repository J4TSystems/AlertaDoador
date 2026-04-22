import enum

from models.donor_model import Base
from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.sql import func


class BloodType(str, enum.Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class StockStatus(str, enum.Enum):
    CRITICAL = "Critical"
    ALERT = "Alert"
    LOW = "Low"
    STABLE = "Stable"


class BloodStock(Base):
    __tablename__ = "blood_stocks"

    blood_type = Column(Enum(BloodType), primary_key=True, index=True)
    status = Column(Enum(StockStatus), nullable=False)
    last_updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
