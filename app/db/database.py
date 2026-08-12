from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from collections.abc import Generator


DATABASE_URL = (
    "postgresql+psycopg://"
    "palm_mind:palm_mind@localhost:5432/palm_mind"
)


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


from app.db import models