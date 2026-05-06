import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["OPENAI_API_KEY"] = ""

from app.database import get_session  # noqa: E402
from app.main import app  # noqa: E402
from app import models  # noqa: F401,E402


@pytest.fixture
def session() -> Session:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as test_session:
        yield test_session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client(session: Session) -> TestClient:
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
