from fastapi import FastAPI

from app.db.database import Base, engine
from app.routes.url import router as url_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="URL Shortener API",
    description="A URL shortening service built with FastAPI",
    version="1.0.0"
)


app.include_router(url_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to URL Shortener API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }