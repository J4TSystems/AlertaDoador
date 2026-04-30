from datetime import datetime
from typing import List

from dtos.stock_dto import BloodStockDTO
from models.blood_stock_model import BloodStock
from repositories.stock_repository import StockRepository
from scrapers.prosangue_scraper import ProSangueScraper, StockClassifier


class StockService:
    def __init__(self, repository: StockRepository):
        self.repository = repository

    def get_all_stock_levels(self) -> List[BloodStockDTO]:
        """
        Return all blood stock levels from the repository.
        """
        stocks = self.repository.get_all()
        return [
            BloodStockDTO(
                blood_type=stock.blood_type,
                status=stock.status,
                last_updated=stock.last_updated,
            )
            for stock in stocks
        ]

    def sync_with_external_source(self) -> List[BloodStockDTO]:
        """
        Sync blood stock data from an external source.
        """
        mapped_data = ProSangueScraper.scrape_mapped_data()
        if not mapped_data:
            return []

        dtos = []
        now = datetime.now()

        for data in mapped_data:
            blood_type = data["blood_type"]
            qty = data["quantity"]
            ref = data["reference"]

            status = StockClassifier.classify(qty, ref)

            dto = BloodStockDTO(blood_type=blood_type, status=status, last_updated=now)
            dtos.append(dto)

            model = BloodStock(
                blood_type=dto.blood_type,
                status=dto.status,
                last_updated=dto.last_updated,
            )
            self.repository.upsert(model)

        return dtos
