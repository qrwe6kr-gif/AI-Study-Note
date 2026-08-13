# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# 1. User 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# 2. Note 스키마 (여기에 NoteResponse가 정확히 들어있어야 합니다!)
class NoteBase(BaseModel):
    title: str
    category: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    user_id: int
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 3. AI Chat 스키마
class ChatRequest(BaseModel):
    note_id: int
    message: str

class ChatResponse(BaseModel):
    id: int
    note_id: int
    sender: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True