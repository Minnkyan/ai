pip install --upgrade openai
import streamlit as st
import openai

# OpenAI API Key를 입력받는 함수
def get_api_key():
    return st.text_input("Enter OpenAI API Key:", type="password")

# @st.cache_data를 사용하여 캐싱된 결과를 반환하는 함수
@st.cache_data
def get_gpt_response(api_key, user_input):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message['content']

# 세션 상태에 API Key를 저장
if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""

if st.session_state["api_key"] == "":
    st.session_state["api_key"] = get_api_key()

if st.session_state["api_key"]:
    user_input = st.text_input("Enter your question:")
    if st.button("Submit"):
        if user_input:
            response = get_gpt_response(st.session_state["api_key"], user_input)
            st.write(response)
        else:
            st.write("Please enter a question.")
