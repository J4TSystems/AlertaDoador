from dtos.donor_dto import BloodType, DonorCreate
from repositories.donor_repository import DonorRepository


def test_get_by_blood_types(db):
    repo = DonorRepository(db)

    # Create donors with different blood types
    donor1 = DonorCreate(
        full_name="Donor 1", email="donor1@example.com", blood_type=BloodType.A_POS
    )
    donor2 = DonorCreate(
        full_name="Donor 2", email="donor2@example.com", blood_type=BloodType.B_POS
    )
    donor3 = DonorCreate(
        full_name="Donor 3", email="donor3@example.com", blood_type=BloodType.O_NEG
    )

    repo.create(donor1)
    repo.create(donor2)
    repo.create(donor3)

    # Test getting donors by blood types A+ and B+
    donors = repo.get_by_blood_types([BloodType.A_POS, BloodType.B_POS])

    assert len(donors) == 2
    blood_types = [d.blood_type for d in donors]
    assert BloodType.A_POS in blood_types
    assert BloodType.B_POS in blood_types
    assert BloodType.O_NEG not in blood_types


def test_get_by_blood_types_empty_list(db):
    repo = DonorRepository(db)

    donor1 = DonorCreate(
        full_name="Donor 1", email="donor1@example.com", blood_type=BloodType.A_POS
    )
    repo.create(donor1)

    donors = repo.get_by_blood_types([])
    assert len(donors) == 0


def test_get_by_blood_types_no_match(db):
    repo = DonorRepository(db)

    donor1 = DonorCreate(
        full_name="Donor 1", email="donor1@example.com", blood_type=BloodType.A_POS
    )
    repo.create(donor1)

    donors = repo.get_by_blood_types([BloodType.B_POS])
    assert len(donors) == 0
