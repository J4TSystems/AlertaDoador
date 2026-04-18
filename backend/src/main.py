from config.database import init_db
from controllers.donor_controller import router as donor_router
from exceptions.exception_handlers import register_exception_handlers
from fastapi import FastAPI
from models.donor_model import Base

# Initialize database
init_db(Base)

app = FastAPI(title="Blood Donation System API")

register_exception_handlers(app)

app.include_router(donor_router)


@app.get("/")
def read_root():
    return {"message": "Blood Donation System API is running"}
