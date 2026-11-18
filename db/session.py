from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import db_url

engine = create_engine(db_url)

SessionLocal = sessionmaker[Session](bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
