from unittest.mock import MagicMock

from email_infra.interfaces.email_provider import EmailProvider
from models.blood_stock_model import BloodStock, BloodType, StockStatus
from models.donor_model import DonorModel
from models.notification_model import NotificationLog
from repositories.donor_repository import DonorRepository
from repositories.notification_repository import NotificationRepository
from repositories.stock_repository import StockRepository
from services.notification_service import NotificationService


def test_process_critical_notifications_sends_email_and_saves_log(db):
    # Arrange (AAA Pattern)

    # 1. Mock Email Provider
    email_provider_mock = MagicMock(spec=EmailProvider)
    email_provider_mock.send_email.return_value = True

    notification_repo = NotificationRepository(db)
    stock_repo = StockRepository(db)
    donor_repo = DonorRepository(db)

    service = NotificationService(
        notification_repo, stock_repo, donor_repo, email_provider_mock
    )

    # 2. Setup a critical blood stock scenario
    critical_stock = BloodStock(blood_type=BloodType.O_NEG, status=StockStatus.CRITICAL)
    db.add(critical_stock)

    # 3. Setup a donor with matching blood type
    donor = DonorModel(
        full_name="John Doe", email="john@example.com", blood_type=BloodType.O_NEG
    )
    db.add(donor)
    db.commit()

    # Act
    results = service.process_critical_notifications()

    # Assert

    # Verify send_email was called with the correct AlertaDoador parameters
    email_provider_mock.send_email.assert_called_once()
    args, _ = email_provider_mock.send_email.call_args
    recipient, subject, body = args

    assert recipient == "john@example.com"
    assert "Urgent: Blood Type O- Needed" in subject
    assert "John Doe" in body
    assert "critical shortage" in body

    # Verify the log was saved in the database
    assert len(results) == 1
    assert results[0].recipient_email == "john@example.com"

    logs = db.query(NotificationLog).all()
    assert len(logs) == 1
    assert logs[0].recipient_email == "john@example.com"
    assert logs[0].blood_type == BloodType.O_NEG


def test_process_critical_notifications_failed_email_does_not_save_log(db):
    # Arrange
    email_provider_mock = MagicMock(spec=EmailProvider)
    email_provider_mock.send_email.return_value = False  # Email failed

    notification_repo = NotificationRepository(db)
    stock_repo = StockRepository(db)
    donor_repo = DonorRepository(db)

    service = NotificationService(
        notification_repo, stock_repo, donor_repo, email_provider_mock
    )

    critical_stock = BloodStock(blood_type=BloodType.A_POS, status=StockStatus.CRITICAL)
    db.add(critical_stock)

    donor = DonorModel(
        full_name="Jane Doe", email="jane@example.com", blood_type=BloodType.A_POS
    )
    db.add(donor)
    db.commit()

    # Act
    results = service.process_critical_notifications()

    # Assert
    email_provider_mock.send_email.assert_called_once()

    # Log should NOT be saved if email failed
    assert len(results) == 0
    logs = db.query(NotificationLog).all()
    assert len(logs) == 0
