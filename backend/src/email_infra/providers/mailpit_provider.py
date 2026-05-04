import smtplib
from email.mime.text import MIMEText

from email_infra.interfaces.email_provider import EmailProvider


class MailpitProvider(EmailProvider):
    def __init__(self, host: str = "mailpit", port: int = 1025):
        self.host = host
        self.port = port
        self.sender = "noreply@alertadoador.com"

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = recipient

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.sendmail(self.sender, [recipient], msg.as_string())
            return True
        except Exception as e:
            # In a real app we would use a logger here
            print(f"Failed to send email: {e}")
            return False
