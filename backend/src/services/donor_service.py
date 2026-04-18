from typing import List
from repositories.donor_repository import DonorRepository
from dtos.donor_dto import DonorCreate
from models.donor_model import DonorModel
from exceptions.business_exceptions import EntityAlreadyExistsError, EntityNotFoundError

class DonorService:
    def __init__(self, donor_repository: DonorRepository):
        self.donor_repository = donor_repository

    def create_donor(self, donor_data: DonorCreate) -> DonorModel:
        existing_donor = self.donor_repository.get_by_email(donor_data.email)
        if existing_donor:
            raise EntityAlreadyExistsError(
                detail="Email already registered"
            )
        
        return self.donor_repository.create(donor_data)

    def get_all_donors(self) -> List[DonorModel]:
        return self.donor_repository.get_all()

    def get_donor_by_id(self, donor_id: int) -> DonorModel:
        donor = self.donor_repository.get_by_id(donor_id)
        if not donor:
            raise EntityNotFoundError(detail="Donor not found")
        return donor

    def delete_donor(self, donor_id: int) -> None:
        donor = self.get_donor_by_id(donor_id)
        self.donor_repository.delete(donor)
