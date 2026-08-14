from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import get_settings 

DB_URL = get_settings().database_url

engine = create_engine(DB_URL)

class Base(DeclarativeBase):
    pass

session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    try:
        with session_local as session:
            yield session
    finally:
        session.close()