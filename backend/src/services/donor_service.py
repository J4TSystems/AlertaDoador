from typing import List

from dtos.donor_dto import DonorCreate
from exceptions.business_exceptions import EntityAlreadyExistsError, EntityNotFoundError
from models.donor_model import DonorModel
from repositories.donor_repository import DonorRepository


class DonorService:
    """
    Service class for donor operations.
    """

    def __init__(self, donor_repository: DonorRepository):
        self.donor_repository = donor_repository

    def create_donor(self, donor_data: DonorCreate) -> DonorModel:
        """
        Create a new donor if the email is not already registered.
        """
        existing_donor = self.donor_repository.get_by_email(donor_data.email)
        if existing_donor:
            raise EntityAlreadyExistsError(detail="Email already registered")

        return self.donor_repository.create(donor_data)

    def get_all_donors(self) -> List[DonorModel]:
        """
        Retrieve all donors.
        """
        return self.donor_repository.get_all()

    def get_donor_by_id(self, donor_id: int) -> DonorModel:
        """
        Retrieve a donor by their ID.
        """
        donor = self.donor_repository.get_by_id(donor_id)
        if not donor:
            raise EntityNotFoundError(detail="Donor not found")
        return donor

    def delete_donor(self, donor_id: int) -> None:
        """
        Delete a donor by their ID.
        """
        donor = self.get_donor_by_id(donor_id)
        self.donor_repository.delete(donor)
