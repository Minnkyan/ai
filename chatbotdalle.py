import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

def generate_image(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
        return None

# 사이드바에 OpenAI API 키 입력란 추가
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# 챗봇 섹션
st.title("챗봇")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API 키를 입력하세요.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message['content']
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {e}")

# DALL-E 이미지 생성 섹션
st.title("DALL-E 이미지 생성기")
st.write("OpenAI의 DALL-E를 사용하여 이미지를 생성합니다.")

if openai_api_key:
    user_prompt = st.text_input("이미지 생성을 위한 프롬프트를 입력하세요:")

    if user_prompt:
        if st.button("이미지 생성"):
            img = generate_image(user_prompt, openai_api_key)
            if img:
                st.image(img, caption='DALL-E 이미지', use_column_width=True)









