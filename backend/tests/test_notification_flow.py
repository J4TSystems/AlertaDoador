from fastapi import status
from models.blood_stock_model import BloodStock, BloodType, StockStatus
from models.donor_model import DonorModel


def test_trigger_notifications_flow(client, db):
    # Arrange
    # 1. Setup Blood Stocks
    stocks = [
        BloodStock(blood_type=BloodType.A_POS, status=StockStatus.CRITICAL),
        BloodStock(blood_type=BloodType.B_POS, status=StockStatus.LOW),
        BloodStock(blood_type=BloodType.O_POS, status=StockStatus.STABLE),
    ]
    for stock in stocks:
        db.add(stock)

    # 2. Setup Donors
    donors = [
        DonorModel(
            full_name="Donor A+", email="a_pos@example.com", blood_type=BloodType.A_POS
        ),
        DonorModel(
            full_name="Donor B+", email="b_pos@example.com", blood_type=BloodType.B_POS
        ),
        DonorModel(
            full_name="Donor O+", email="o_pos@example.com", blood_type=BloodType.O_POS
        ),
    ]
    for donor in donors:
        db.add(donor)

    db.commit()

    # Act
    response = client.post("/notifications/send-alerts")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # We expect 2 notifications: for A+ (CRITICAL) and B+ (LOW).
    # O+ is STABLE, so no notification.
    assert len(data) == 2

    emails = [log["recipient_email"] for log in data]
    assert "a_pos@example.com" in emails
    assert "b_pos@example.com" in emails
    assert "o_pos@example.com" not in emails

    # Verify mapping
    for log in data:
        if log["recipient_email"] == "a_pos@example.com":
            assert log["blood_type"] == "A+"
            assert log["status_at_time"] == "Critical"
        if log["recipient_email"] == "b_pos@example.com":
            assert log["blood_type"] == "B+"
            assert log["status_at_time"] == "Low"


def test_trigger_notifications_no_critical_stock(client, db):
    # Arrange
    db.add(BloodStock(blood_type=BloodType.A_POS, status=StockStatus.STABLE))
    db.add(
        DonorModel(
            full_name="Donor A+", email="a_pos@example.com", blood_type=BloodType.A_POS
        )
    )
    db.commit()

    # Act
    response = client.post("/notifications/send-alerts")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0
