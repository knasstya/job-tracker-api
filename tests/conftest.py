import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app
from app.core.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_job():
    return {
        "company": "Google",
        "position": "Backend Developer"
    }


@pytest.fixture
def authenticated_client(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 201

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return client

@pytest.fixture
def client_factory(client):
    clients = []

    def create_client():
        test_client = TestClient(app)
        clients.append(test_client)
        return test_client

    yield create_client

    for test_client in clients:
        test_client.close()

@pytest.fixture
def create_authenticated_client(client_factory):
    def create(email):
        client = client_factory()

        response = client.post(
            "/auth/register",
            json={
                "email": email,
                "password": "secret123"
            }
        )

        assert response.status_code == 201

        response = client.post(
            "/auth/login",
            data={
                "username": email,
                "password": "secret123"
            }
        )

        assert response.status_code == 200

        token = response.json()["access_token"]

        client.headers.update({
            "Authorization": f"Bearer {token}"
        })

        return client

    return create