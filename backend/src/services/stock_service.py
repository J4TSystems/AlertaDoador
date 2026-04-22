from datetime import datetime
from typing import Dict, List

from dtos.stock_dto import BloodStockDTO
from models.blood_stock_model import BloodType, StockStatus
from repositories.stock_repository import StockRepository


class StockService:
    def __init__(self, repository: StockRepository):
        self.repository = repository

    def get_all_stock_levels(self) -> List[BloodStockDTO]:
        """
        Return a hardcoded list of 1 or 2 BloodStockDTO objects.
        """
        return [
            BloodStockDTO(
                blood_type=BloodType.A_POS,
                status=StockStatus.STABLE,
                last_updated=datetime.now(),
            ),
            BloodStockDTO(
                blood_type=BloodType.O_NEG,
                status=StockStatus.CRITICAL,
                last_updated=datetime.now(),
            ),
        ]

    def sync_with_external_source(self) -> Dict[str, str]:
        """
        Return a simple dictionary message.
        """
        return {"message": "Sync triggered successfully"}
