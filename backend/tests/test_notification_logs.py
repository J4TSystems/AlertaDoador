import uuid

from models.blood_stock_model import BloodType, StockStatus
from models.notification_model import NotificationLog


def test_get_sent_logs_empty(client, db):
    # Act
    response = client.get("/notifications/history")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_get_sent_logs_with_data(client, db):
    # Arrange
    log1 = NotificationLog(
        id=str(uuid.uuid4()),
        recipient_email="donor1@example.com",
        blood_type=BloodType.A_POS,
        status_at_time=StockStatus.CRITICAL,
    )
    log2 = NotificationLog(
        id=str(uuid.uuid4()),
        recipient_email="donor2@example.com",
        blood_type=BloodType.B_POS,
        status_at_time=StockStatus.LOW,
    )
    db.add(log1)
    db.add(log2)
    db.commit()

    # Act
    response = client.get("/notifications/history")

    # Assert
    assert response.status_code == 200
    data = response.json()
    # Atualmente retorna [], então este teste deve falhar se houver dados
    assert len(data) == 2
    emails = [log["recipient_email"] for log in data]
    assert "donor1@example.com" in emails
    assert "donor2@example.com" in emails
