from typing import List, Optional

from dtos.donor_dto import BloodType, DonorCreate
from models.donor_model import DonorModel
from sqlalchemy.orm import Session


class DonorRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donor_data: DonorCreate) -> DonorModel:
        db_donor = DonorModel(
            full_name=donor_data.full_name,
            email=donor_data.email,
            blood_type=donor_data.blood_type,
        )
        self.db.add(db_donor)
        self.db.commit()
        self.db.refresh(db_donor)
        return db_donor

    def get_by_id(self, donor_id: int) -> Optional[DonorModel]:
        return self.db.query(DonorModel).filter(DonorModel.id == donor_id).first()

    def get_by_email(self, email: str) -> Optional[DonorModel]:
        return self.db.query(DonorModel).filter(DonorModel.email == email).first()

    def get_all(self) -> List[DonorModel]:
        return self.db.query(DonorModel).all()

    def get_by_blood_types(self, blood_types: List[BloodType]) -> List[DonorModel]:
        return (
            self.db.query(DonorModel)
            .filter(DonorModel.blood_type.in_(blood_types))
            .all()
        )

    def delete(self, donor: DonorModel) -> None:
        self.db.delete(donor)
        self.db.commit()
