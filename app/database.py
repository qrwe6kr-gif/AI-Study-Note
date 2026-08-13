# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 파일 위치 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# DB 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# DB 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 (이후 models.py에서 DB 테이블 정의할 때 상속받음)
Base = declarative_base()

# DB 세션 의존성 함수 (API 호출 시 DB 연결하고 끝나면 닫아줌)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()