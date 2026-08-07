from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user: UserCreate
    ):

        existing_user = UserRepository.get_by_email(
            db,
            user.email
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        return UserRepository.create(
            db,
            user
        )