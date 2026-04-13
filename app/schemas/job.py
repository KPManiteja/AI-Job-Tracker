from pydantic import BaseModel
from typing import Optional

class JobCreate(BaseModel):
    company: str
    role: str


class JobUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None

class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str

    class Config:
        from_attributes = True