import os

from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(Base):
    """Initializes the database by creating tables (skips if testing)."""
    if os.getenv("TESTING") == "True":
        return

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
