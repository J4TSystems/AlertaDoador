from datetime import datetime

from models.blood_stock_model import BloodType, StockStatus
from pydantic import BaseModel


class BloodStockDTO(BaseModel):
    blood_type: BloodType
    status: StockStatus
    last_updated: datetime

    class Config:
        from_attributes = True


class SyncResponse(BaseModel):
    message: str
