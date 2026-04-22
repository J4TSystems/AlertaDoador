from typing import List

from models.blood_stock_model import BloodStock
from sqlalchemy.orm import Session


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[BloodStock]:
        pass

    def save(self, stock: BloodStock) -> BloodStock:
        pass
