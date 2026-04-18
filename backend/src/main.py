import os
from fastapi import FastAPI
from controllers.donor_controller import router as donor_router
from config.database import init_db
from models.donor_model import Base
from exceptions.exception_handlers import register_exception_handlers

# Initialize database
init_db(Base)

app = FastAPI(title="Blood Donation System API")

register_exception_handlers(app)

app.include_router(donor_router)

@app.get("/")
def read_root():
    return {"message": "Blood Donation System API is running"}
