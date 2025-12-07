"""Database session and engine configuration."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Iterator[Session]:
    """FastAPI dependency that yields a database session.

    The session is committed/closed by the caller when appropriate. Using a
    generator with ``try/finally`` guarantees the connection is released back
    to the pool even when an exception bubbles up from request handling.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
