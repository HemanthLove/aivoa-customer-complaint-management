from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.complaints import router as complaints_router
from app.database.database import engine
from app.models.base import Base
from app.models.complaint import Complaint


# Create database tables if they do not already exist.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AIVOA Customer Complaint Management API",
    version="1.0.0",
)


# Allow the React frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(complaints_router)


@app.get("/")
def root():
    return {
        "service": "AIVOA Customer Complaint Management API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "aivoa-api",
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect():
            return {
                "status": "ok",
                "database": "connected",
            }
    except Exception as error:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(error),
        }