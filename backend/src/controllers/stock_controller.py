from typing import List

from config.database import get_db
from dtos.stock_dto import BloodStockDTO
from fastapi import APIRouter, Depends, status
from repositories.stock_repository import StockRepository
from services.stock_service import StockService
from sqlalchemy.orm import Session

"""
    Manages blood stock levels, coordinates web scraping sync
    and exposes real-time inventory data.
"""
router = APIRouter(prefix="/stock", tags=["Blood Stock"])


def get_stock_service(db: Session = Depends(get_db)) -> StockService:
    repository = StockRepository(db)
    return StockService(repository)


@router.get("/", response_model=List[BloodStockDTO])
def get_stock(service: StockService = Depends(get_stock_service)):
    return service.get_all_stock_levels()


@router.post("/sync", status_code=status.HTTP_200_OK)
def sync_stock(service: StockService = Depends(get_stock_service)):
    return service.sync_with_external_source()
