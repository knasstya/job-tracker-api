def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "created_at" in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "secret123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherpassword"
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already registered"
    }

def test_login_user(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "secret123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["access_token"]
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrongpassword@example.com",
            "password": "secret123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "wrongpassword@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }

def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid credentials"
    }

def test_protected_endpoint_without_token(client):
    response = client.get("/jobs/")

    assert response.status_code == 401

def test_protected_endpoint_with_invalid_token(client):
    client.headers.update({
        "Authorization": "Bearer this-is-not-a-valid-jwt"
    })

    response = client.get("/jobs/")

    assert response.status_code == 401


from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from app.core.jwt import ALGORITHM


def test_protected_endpoint_with_expired_token(client):
    expired_token = jwt.encode(
        {
            "sub": "test@example.com",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
        },
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    client.headers.update({
        "Authorization": f"Bearer {expired_token}"
    })

    response = client.get("/jobs/")

    assert response.status_code == 401

def test_password_is_hashed(client, db):
    response = client.post(
        "/auth/register",
        json={
            "email": "hashed@example.com",
            "password": "secret123"
        }
    )

    assert response.status_code == 201

    from app.repositories.user_repository import UserRepository

    user = UserRepository.get_by_email(
        db,
        "hashed@example.com"
    )

    assert user is not None
    assert user.hashed_password != "secret123"
    assert user.hashed_password.startswith("$2")