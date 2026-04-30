from typing import List

from models.blood_stock_model import BloodStock
from sqlalchemy.orm import Session


class StockRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[BloodStock]:
        return self.db.query(BloodStock).all()

    def save(self, stock: BloodStock) -> BloodStock:
        self.db.add(stock)
        self.db.commit()
        self.db.refresh(stock)
        return stock

    def upsert(self, stock_data: BloodStock) -> BloodStock:
        existing_stock = (
            self.db.query(BloodStock)
            .filter(BloodStock.blood_type == stock_data.blood_type)
            .first()
        )

        if existing_stock:
            existing_stock.status = stock_data.status
            existing_stock.last_updated = stock_data.last_updated
            self.db.commit()
            self.db.refresh(existing_stock)
            return existing_stock
        else:
            return self.save(stock_data)
