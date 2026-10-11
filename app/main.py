
from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.certificates import router as certificates_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CertiFlow API",
    description="Bulk Certificate Generation and Tracking API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CertiFlow API",
        "docs": "/docs"
    }


app.include_router(certificates_router)
