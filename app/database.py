from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import DATABASE_URL, IS_SQLITE

DATABASE_URL = "mysql+pymysql://root:1234@localhost/lab1"

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


_engine_args = {}
if IS_SQLITE:
    # Needed for SQLite when used with FastAPI (multithreaded)
    _engine_args["connect_args"] = {"check_same_thread": False}
else:
    # Recommended for MySQL to avoid stale connections
    _engine_args["pool_pre_ping"] = True

engine = create_engine(DATABASE_URL, **_engine_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency that provides a SQLAlchemy session and ensures proper close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
