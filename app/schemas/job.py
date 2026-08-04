from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    position: str

class JobUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    status: str | None = None

class JobResponse(BaseModel):
    id: int
    company: str
    position: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True