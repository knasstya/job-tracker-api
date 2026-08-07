from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict
):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM]
    )