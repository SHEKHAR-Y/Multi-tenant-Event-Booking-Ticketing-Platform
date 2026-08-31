import pytest

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool 
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient 

from app.core.database import Base, get_db
from app.main import app


TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

testing_local_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def override_get_db():
    with testing_local_session() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def db_session():
    with testing_local_session() as session:
        yield session