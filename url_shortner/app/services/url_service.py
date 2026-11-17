import secrets
import string

from sqlalchemy.orm import Session

from app.db.models import URL


ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int = 7) -> str:
    return "".join(
        secrets.choice(ALPHABET)
        for _ in range(length)
    )


def create_short_url(db: Session, original_url: str):
    # Generate a unique short code
    while True:
        short_code = generate_short_code()

        existing_url = db.query(URL).filter(
            URL.short_code == short_code
        ).first()

        if not existing_url:
            break

    # Create database record
    new_url = URL(
        original_url=str(original_url),
        short_code=short_code
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url


def get_original_url(db: Session, short_code: str):
    return db.query(URL).filter(
        URL.short_code == short_code
    ).first()


def increment_clicks(db: Session, url: URL):
    url.clicks += 1
    db.commit()
    db.refresh(url)