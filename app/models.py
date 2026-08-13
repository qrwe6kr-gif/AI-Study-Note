# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정 (1:N)
    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)  # AI가 생성할 3줄 요약
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    owner = relationship("User", back_populates="notes")
    chat_histories = relationship("ChatHistory", back_populates="note", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="note", cascade="all, delete-orphan")


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    sender = Column(String(10), nullable=False)  # 'user' 또는 'ai'
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 관계 설정
    note = relationship("Note", back_populates="chat_histories")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)  # 보기 목록
    answer = Column(Text, nullable=False)  # 정답
    explanation = Column(Text, nullable=True)  # AI의 해설

    # 관계 설정
    note = relationship("Note", back_populates="quizzes")