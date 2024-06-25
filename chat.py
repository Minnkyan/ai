import streamlit as st
from streamlit_chat import message

# 메모리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 저장한 메시지 사용자/응답 구분해서 보여주기
for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")

# 사용자 입력과 LLM 응답
if prompt := st.chat_input("What is up?"):
    # 사용자 메시지 보여주기
    message(prompt, is_user=True)
    
    # 메모리에 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Echo 챗봇 응답
    response = f"Echo: {prompt}"
    
    # LLM 응답 보여주기
    message(response, is_user=False)
    
    # 메모리에 LLM 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response})




