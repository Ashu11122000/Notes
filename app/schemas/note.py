from pydantic import BaseModel
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponse(NoteBase):
    id: int
    owner_id: int                   
    created_at: datetime
    updated_at: datetime | None = None  

    class Config:
        from_attributes = True        