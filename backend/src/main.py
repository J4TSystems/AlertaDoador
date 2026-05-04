import logging

from config.database import init_db
from controllers.donor_controller import router as donor_router
from controllers.notification_controller import router as notification_router
from controllers.stock_controller import router as stock_router
from exceptions.exception_handlers import register_exception_handlers
from fastapi import FastAPI
from models.donor_model import Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize database
init_db(Base)

app = FastAPI(title="Blood Donation System API")

register_exception_handlers(app)

app.include_router(donor_router)
app.include_router(stock_router)
app.include_router(notification_router)


@app.get("/")
def read_root():
    return {"message": "Blood Donation System API is running"}
