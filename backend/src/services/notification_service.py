import logging
import uuid
from typing import List

from dtos.notification_dto import NotificationLogDTO
from email_infra.interfaces.email_provider import EmailProvider
from models.blood_stock_model import StockStatus
from models.notification_model import NotificationLog
from repositories.donor_repository import DonorRepository
from repositories.notification_repository import NotificationRepository
from repositories.stock_repository import StockRepository

logger = logging.getLogger(__name__)


def build_donor_alert(donor_name: str, blood_type: str) -> tuple[str, str]:
    subject = f"Urgente: Tipo Sanguíneo {blood_type} Necessário na Pró-Sangue"
    body = (
        f"Olá {donor_name},\n\n"
        "Nosso sistema (AlertaDoador) identificou um estoque crítico para o seu "
        f"tipo sanguíneo ({blood_type}).\n"
        "Sua doação pode salvar vidas. Por favor, considere visitar o posto da "
        "Pró-Sangue mais próximo o quanto antes.\n\n"
        "Agradecemos o seu apoio,\n"
        "Equipe AlertaDoador\n"
    )
    return subject, body


class NotificationService:
    def __init__(
        self,
        repository: NotificationRepository,
        stock_repository: StockRepository,
        donor_repository: DonorRepository,
        email_provider: EmailProvider,
    ):
        self.repository = repository
        self.stock_repository = stock_repository
        self.donor_repository = donor_repository
        self.email_provider = email_provider

    def process_critical_notifications(self) -> List[NotificationLogDTO]:
        """
        Processes critical blood stock notifications and sends alerts to donors.
        """
        logger.info("Starting process_critical_notifications")
        # 1. Retrieve all stock levels
        stock_blood = self.stock_repository.get_all()
        logger.info(f"Retrieved {len(stock_blood)} stock records")

        # 2. Filter locally: keep only items where status is CRITICAL or LOW
        stock_blood_filtered = [
            s
            for s in stock_blood
            if s.status in [StockStatus.CRITICAL, StockStatus.LOW, StockStatus.ALERT]
        ]
        logger.info(f"Found {len(stock_blood_filtered)} critical or low stocks")

        # 3. Extract blood types
        blood_types = [s.blood_type for s in stock_blood_filtered]

        if not blood_types:
            logger.info("No critical or low stocks found. Skipping donor notification.")
            return []

        # 4. Fetch donors
        donors = self.donor_repository.get_by_blood_types(blood_types)
        logger.info(f"Fetched {len(donors)} donors to notify")

        # Map stock status by blood type for quick lookup
        stock_map = {s.blood_type: s.status for s in stock_blood_filtered}

        notification_logs = []

        # 5. Create logs and send emails
        for donor in donors:
            logger.info(
                "Creating notification for donor %s (Blood Type: %s)",
                donor.email,
                donor.blood_type,
            )

            # Generate subject and body
            blood_type_str = (
                donor.blood_type.value
                if hasattr(donor.blood_type, "value")
                else donor.blood_type
            )
            subject, body = build_donor_alert(donor.full_name, blood_type_str)

            # Call email provider
            email_sent = self.email_provider.send_email(donor.email, subject, body)

            if email_sent:
                log = NotificationLog(
                    id=str(uuid.uuid4()),
                    recipient_email=donor.email,
                    blood_type=donor.blood_type,
                    status_at_time=stock_map[donor.blood_type],
                )
                # 6. Save logs
                saved_log = self.repository.save(log)
                notification_logs.append(NotificationLogDTO.model_validate(saved_log))
            else:
                logger.error(f"Failed to send email to {donor.email}. Log not saved.")

        # 7. Return
        logger.info(f"Process completed. {len(notification_logs)} notifications sent.")
        return notification_logs

    def get_sent_logs(self) -> List[NotificationLogDTO]:
        """
        Retrieves all sent notification logs.
        """
        logs = self.repository.get_all()
        return [NotificationLogDTO.model_validate(log) for log in logs]
