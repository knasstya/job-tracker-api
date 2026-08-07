from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return AuthService.register_user(
        db,
        user
    )

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=200
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    return AuthService.login_user(
        db,
        user.email,
        user.password
    )