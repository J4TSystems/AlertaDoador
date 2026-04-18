from enum import Enum

from pydantic import BaseModel, EmailStr


class BloodType(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class DonorCreate(BaseModel):
    full_name: str
    email: EmailStr
    blood_type: BloodType


class DonorRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    blood_type: BloodType

    class Config:
        from_attributes = True
