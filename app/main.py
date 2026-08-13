# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, get_db
from app import models, schemas
from app.ai_service import generate_summary, ask_ai_about_note, generate_quizzes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Note API")

# 💡 CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용 (개발용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI 개인 학습 노트 백엔드 서버가 정상 구동 중입니다!"}

# ----- 1. 노트 관련 API -----

@app.post("/notes/", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == 1).first()
    if not db_user:
        db_user = models.User(email="test@example.com", hashed_password="testpassword")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # AI 요약 생성 연동
    ai_summary = generate_summary(note.content)

    db_note = models.Note(
        user_id=db_user.id,
        title=note.title,
        category=note.category,
        content=note.content,
        summary=ai_summary
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/", response_model=List[schemas.NoteResponse])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Note).offset(skip).limit(limit).all()

@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")
    return db_note

# ----- 2. AI 챗봇 API -----

@app.post("/notes/{note_id}/chat", response_model=schemas.ChatResponse)
def chat_with_note(note_id: int, chat_req: schemas.ChatRequest, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    # 사용자 질문 저장
    user_chat = models.ChatHistory(
        note_id=note_id,
        sender="user",
        message=chat_req.message
    )
    db.add(user_chat)
    db.commit()

    # 이전 대화 기록 가져오기 (최근 10개)
    history = db.query(models.ChatHistory).filter(
        models.ChatHistory.note_id == note_id
    ).order_by(models.ChatHistory.created_at.asc()).all()

    # AI 답변 생성
    ai_reply = ask_ai_about_note(db_note.content, history, chat_req.message)

    # AI 답변 DB 저장
    ai_chat = models.ChatHistory(
        note_id=note_id,
        sender="ai",
        message=ai_reply
    )
    db.add(ai_chat)
    db.commit()
    db.refresh(ai_chat)

    return ai_chat

# ----- 3. AI 퀴즈 생성 API -----

@app.post("/notes/{note_id}/quizzes")
def create_quizzes_for_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="노트를 찾을 수 없습니다.")

    quizzes_data = generate_quizzes(db_note.content)
    
    saved_quizzes = []
    for q in quizzes_data:
        quiz = models.Quiz(
            note_id=note_id,
            question=q.get("question", ""),
            options=q.get("options", []),
            answer=q.get("answer", ""),
            explanation=q.get("explanation", "")
        )
        db.add(quiz)
        saved_quizzes.append(quiz)

    db.commit()
    return {"message": f"{len(saved_quizzes)}개의 AI 퀴즈가 성공적으로 생성되었습니다.", "quizzes": quizzes_data}