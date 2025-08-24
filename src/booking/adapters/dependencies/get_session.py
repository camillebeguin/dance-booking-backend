from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from fastapi import Depends


def get_db_url() -> str:
    return "postgresql+psycopg2://dev:dev@localhost:5432/booking-db"


def get_db_session(db_url: str = Depends(get_db_url)) -> Generator[Session, None, None]:
    """
    Get SQLAlchemy database session.
    """
    engine = create_engine(db_url)
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()
