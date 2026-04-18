from typing import List

from config.database import get_db
from dtos.donor_dto import DonorCreate, DonorRead
from fastapi import APIRouter, Depends, status
from repositories.donor_repository import DonorRepository
from services.donor_service import DonorService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/donors", tags=["donors"])


def get_donor_service(db: Session = Depends(get_db)) -> DonorService:
    repository = DonorRepository(db)
    return DonorService(repository)


@router.post("/", response_model=DonorRead, status_code=status.HTTP_201_CREATED)
def create_donor(
    donor: DonorCreate, service: DonorService = Depends(get_donor_service)
):
    return service.create_donor(donor)


@router.get("/", response_model=List[DonorRead])
def get_donors(service: DonorService = Depends(get_donor_service)):
    return service.get_all_donors()


@router.get("/{donor_id}", response_model=DonorRead)
def get_donor(donor_id: int, service: DonorService = Depends(get_donor_service)):
    return service.get_donor_by_id(donor_id)


@router.delete("/{donor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donor(donor_id: int, service: DonorService = Depends(get_donor_service)):
    service.delete_donor(donor_id)
