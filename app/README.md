# 📚 AI 연구 노트 (AI Study Note)

FastAPI와 Google Gemini API를 활용한 대학생 학습 노트 및 AI 스터디 튜터 백엔드 서비스입니다.

---

## 🌟 주요 기능

1. **노트 자동 3줄 요약 (`POST /notes/`)**
   - 학습 노트를 작성하면 Gemini AI가 핵심 내용만 3줄로 간결하게 요약하여 저장합니다.

2. **노트 CRUD (`GET /notes/`, `GET /notes/{id}`)**
   - 작성된 학습 노트 목록 및 상세 정보(원문 + AI 요약)를 조회합니다.

3. **노트 기반 AI 스터디 튜터 챗봇 (`POST /notes/{id}/chat`)**
   - 학습 노트의 컨텍스트를 파악하여 궁금한 점에 대해 친절하게 답변해 줍니다.

4. **AI 객관식 퀴즈 자동 생성 (`POST /notes/{id}/quiz`)**
   - 노트 내용을 바탕으로 복습용 객관식 퀴즈 3개를 자동 생성합니다 (JSON Structured Output 적용).

---

## 🛠 기술 스택

- **Backend**: Python, FastAPI, Uvicorn
- **Database**: SQLite, SQLAlchemy
- **AI Engine**: Google GenAI SDK (`google-genai`), Gemini 3.5 Flash / Flash Lite
- **Validation**: Pydantic

---

## 🚀 실행 방법

### 1. 가상환경 및 패키지 설치
```bash
pip install -r requirements.txt