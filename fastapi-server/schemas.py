from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    tags: List[str] = []

class NoteCreate(NoteBase):
    auto_summarize: bool = True  # let client override per-request if needed

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    auto_summarize: bool = True

class NoteOut(NoteBase):
    id: str
    summary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True  # Pydantic v2: enables ORM conversion
