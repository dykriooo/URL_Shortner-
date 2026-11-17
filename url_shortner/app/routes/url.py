from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.url import URLCreate
from app.services.url_service import (
    create_short_url,
    get_original_url,
    increment_clicks
)
from app.core.config import settings


router = APIRouter(prefix="/api/urls", tags=["URL Shortener"])


@router.post("/")
def create_url(
    request: URLCreate,
    db: Session = Depends(get_db)
):
    url = create_short_url(
        db,
        str(request.original_url)
    )

    return {
        "id": url.id,
        "original_url": url.original_url,
        "short_code": url.short_code,
        "short_url": f"{settings.BASE_URL}/{url.short_code}",
        "clicks": url.clicks
    }


@router.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = get_original_url(db, short_code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    increment_clicks(db, url)

    return RedirectResponse(
        url=url.original_url,
        status_code=307
    )


@router.get("/{short_code}/stats")
def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    url = get_original_url(db, short_code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return {
        "original_url": url.original_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "created_at": url.created_at
    }