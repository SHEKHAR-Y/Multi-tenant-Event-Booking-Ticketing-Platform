from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker 

DB_URL =  "postgresql+psycopg2://postgres:ShekhaRpc%4029@localhost:5432/my_database_name"

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