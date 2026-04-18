from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from dtos.donor_dto import BloodType

Base = declarative_base()

class DonorModel(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    blood_type = Column(SQLEnum(BloodType), nullable=False)
