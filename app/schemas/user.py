from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str