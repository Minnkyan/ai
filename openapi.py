import streamlit as st
import openai

# 세션 상태 초기화
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

# OpenAI API Key 입력
api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state["api_key"])

# API Key 저장
st.session_state["api_key"] = api_key

# OpenAI API 클라이언트 생성
if api_key:
    openai.api_key = api_key
else:
    st.error("OpenAI API Key를 입력하세요.")

# 질문 입력
question = st.text_input("질문을 입력하세요.")

# 메모라이징
@st.cache_data
def get_answer(question):
    # GPT-3.5 모델에 질문 전송
    response = openai.Completion.create(engine="davinci-3", prompt=question)

    # 응답 추출
    answer = response["choices"][0]["text"]
    return answer

# 응답 출력
if question:
    answer = get_answer(question)
    st.success(f"GPT-3.5 응답: {answer}")

