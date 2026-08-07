from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String, nullable=False)

    position = Column(String, nullable=False)

    status = Column(
        String,
        default="Applied"
    )

    created_at = Column(
    DateTime,
    default=lambda: datetime.now(timezone.utc)
    )

    user_id = Column(
    Integer,
    ForeignKey("users.id"),
    nullable=False
    )