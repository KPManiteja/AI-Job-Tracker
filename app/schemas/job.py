from pydantic import BaseModel


class JobCreate(BaseModel):
    company: str
    role: str


class JobResponse(BaseModel):
    id: int
    company: str
    role: str
    status: str

    class Config:
        from_attributes = True