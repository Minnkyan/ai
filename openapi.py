import streamlit as st
import openai
from openai import OpenAIError

# OpenAI API 키를 입력받고 session_state에 저장
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

st.session_state['api_key'] = st.text_input("Enter your OpenAI API key:", type="password", value=st.session_state['api_key'])

# OpenAI API 키가 없으면 실행 중지
if not st.session_state['api_key']:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# OpenAI API 설정
openai.api_key = st.session_state['api_key']

# 캐시된 데이터 함수
@st.cache_data(ttl=3600)
def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except OpenAIError as e:
        return f"Error: {str(e)}"

# 사용자 입력 받기
prompt = st.text_input("Ask a question to GPT-3.5-turbo:")

# 질문이 입력되면 응답 받기
if prompt:
    response = get_gpt_response(prompt)
    st.text_area("GPT-3.5-turbo response:", value=response, height=200)
