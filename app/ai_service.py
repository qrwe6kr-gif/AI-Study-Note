# app/ai_service.py
import os
import json
import traceback
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 💡 최신 권장 모델인 gemini-3.5-flash 또는 gemini-flash-latest 자동 지정
def get_available_model():
    try:
        models = list(client.models.list())
        model_names = [m.name.replace("models/", "") for m in models]
        
        # 목록에 있는 최신 정식 모델 우선 순위 체크
        for priority_model in ["gemini-3.5-flash", "gemini-3.6-flash", "gemini-flash-latest"]:
            if priority_model in model_names:
                return priority_model

        for name in model_names:
            if "flash" in name and "2.5" not in name:
                return name
                
        return "gemini-3.5-flash"
    except Exception as e:
        print(f"모델 목록 조회 중 에러: {e}")
        return "gemini-3.5-flash"

# 1. 노트 자동 3줄 요약 기능
def generate_summary(content: str) -> str:
    try:
        target_model = get_available_model()
        print(f"🎯 [최종 선택된 모델]: {target_model}")

        prompt = f"""너는 대학생 학습 노트를 요약해주는 도우미 AI야. 
전달받은 아래 노트 본문을 핵심 내용 위주로 딱 3줄로 간결하게 요약해줘.

[노트 본문]
{content}"""

        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gemini 요약 에러 상세 내용:")
        traceback.print_exc()
        return f"AI 요약을 생성하지 못했습니다. (에러: {e})"

# 2. 노트 기반 AI 챗봇 기능
def ask_ai_about_note(note_content: str, chat_history: list, user_message: str) -> str:
    try:
        target_model = get_available_model()
        system_instruction = f"""너는 학생의 학습 노트를 함께 공부하는 AI 스터디 튜터야.
아래에 제공된 [노트 내용]을 바탕으로 사용자의 질문에 친절하고 이해하기 쉽게 답변해줘.

[노트 내용]
{note_content}"""

        context_str = ""
        for chat in chat_history:
            role_name = "사용자" if chat.sender == "user" else "AI"
            context_str += f"{role_name}: {chat.message}\n"

        prompt = f"[이전 대화 기록]\n{context_str}\n\n사용자 질문: {user_message}"

        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config={"system_instruction": system_instruction}
        )
        return response.text.strip()
    except Exception as e:
        print(f"Gemini 챗봇 에러: {e}")
        return "AI 챗봇 답변을 가져오지 못했습니다."

# 3. AI 퀴즈 자동 생성기
def generate_quizzes(note_content: str) -> list:
    try:
        target_model = get_available_model()
        prompt = f"""전달받은 아래 학습 노트 내용을 바탕으로 학생이 복습할 수 있는 객관식 퀴즈 3개를 만들어줘.
응답은 반드시 아래 JSON 형식으로만 출력해줘.

[
  {{
    "question": "문제 내용",
    "options": ["1번 보기", "2번 보기", "3번 보기", "4번 보기"],
    "answer": "정답 보기 내용",
    "explanation": "해설 설명"
  }}
]

[노트 내용]
{note_content}"""

        response = client.models.generate_content(
            model=target_model,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        return data.get("quizzes", data) if isinstance(data, dict) else data
    except Exception as e:
        print(f"Gemini 퀴즈 생성 에러: {e}")
        return []