import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db:5432/alerta_doador"
    )
    SMTP_HOST: str = os.getenv("SMTP_HOST", "mailpit")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 1025))


settings = Settings()
