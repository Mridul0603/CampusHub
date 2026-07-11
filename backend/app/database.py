from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,       # detect stale connections
    pool_size=10,             # connection pool size
    max_overflow=20,          # extra connections under load
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    FastAPI dependency that yields a DB session per request and
    always closes it afterward — even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
