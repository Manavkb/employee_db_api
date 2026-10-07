"""
database.py - connect to the database.

    engine        -> the connection to the database file
    SessionLocal  -> a factory that creates a new session (a "conversation")
    Base          -> parent class for every table model
    get_db()      -> dependency: one session per request, always closed
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./employees.db"          # a file next to main.py

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},     # needed for SQLite + FastAPI only
)

# Create a database-session factory and call it SessionLocal(variable name)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


# Each API request gets its own temporary database session, and that session is closed after the request.
def get_db():
    db = SessionLocal()   # creating actual session
    try:
        yield db          # the endpoint uses the session here
    finally:
        db.close()        # always closed - Module 04 pattern
