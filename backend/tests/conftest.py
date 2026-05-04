import os
import sys

# Adiciona o diretório src ao path para que os imports funcionem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import MagicMock

import pytest
from config.database import get_db
from controllers.notification_controller import get_notification_service
from email_infra.interfaces.email_provider import EmailProvider
from fastapi import Depends
from fastapi.testclient import TestClient
from main import app
from models.donor_model import Base
from repositories.donor_repository import DonorRepository
from repositories.notification_repository import NotificationRepository
from repositories.stock_repository import StockRepository
from services.notification_service import NotificationService
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = "sqlite://"  # In-memory

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    # Garantir que as tabelas sejam criadas no banco em memória vinculado a este engine
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpar o banco após cada teste para garantir isolamento
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Mock EmailProvider for all tests using the client
    mock_email_provider = MagicMock(spec=EmailProvider)
    mock_email_provider.send_email.return_value = True

    def override_get_notification_service(db_session: Session = Depends(get_db)):
        repository = NotificationRepository(db_session)
        stock_repository = StockRepository(db_session)
        donor_repository = DonorRepository(db_session)
        return NotificationService(
            repository, stock_repository, donor_repository, mock_email_provider
        )

    app.dependency_overrides[get_notification_service] = (
        override_get_notification_service
    )

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
