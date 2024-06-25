import streamlit as st
import openai

# OpenAI API 키 설정
openai.api_key = "sk-proj-GGcJcvRZjvP4I1K8WGoOT3BlbkFJAc9R561FOWTpISLFsFjn"

def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="gpt-4o",  # 사용할 엔진 선택
        prompt=prompt,
        max_tokens=150  # 응답으로 받을 최대 토큰 수
    )
    return response.choices[0].text.strip()

# 메모리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메시지 사용자/응답 구분해서 보여주기
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# 사용자 입력과 LLM 응답
if prompt := st.chat_input("What is up?"):
    # 사용자 메시지 보여주기
    st.chat_message("user").markdown(prompt)
    
    # 메모리에 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # LLM 응답 생성
    response = get_openai_response(prompt)
    
    # LLM 응답 보여주기
    st.chat_message("assistant").markdown(response)
    
    # 메모리에 LLM 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})
