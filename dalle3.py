import streamlit as st
import openai
from PIL import Image
import requests
import io

# Streamlit 페이지 설정
st.set_page_config(page_title="Chatbot and Image Generator", layout="wide")

# Dall-E 이미지 생성을 위한 함수
@st.cache_data(show_spinner=False)
def generate_image(prompt, api_key):
    openai.api_key = api_key
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        return image
    except Exception as e:
        st.error(f"Failed to generate image: {str(e)}")
        return None

# 페이지 선택
page = st.sidebar.selectbox("Choose a page", ["Chatbot", "Image Generator"])

# API 키 입력
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Chatbot 페이지
if page == "Chatbot":
    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not api_key:
            st.warning("Please enter the API key.")
        else:
            openai.api_key = api_key
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response = openai.Completion.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            msg = response.choices[0].message['content']
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)

# 이미지 생성 페이지
elif page == "Image Generator":
    st.title("🖼️ Image Generator")
    if "user_prompt" not in st.session_state:
        st.session_state.user_prompt = ""

    prompt = st.text_input("Enter your prompt for the image", value=st.session_state.user_prompt)
    st.session_state.user_prompt = prompt

    # 이미지 생성 및 표시
    if prompt:
        if not api_key:
            st.warning("Please enter the API key to generate an image.")
        else:
            image = generate_image(prompt, api_key)
            if image:
                st.image(image, caption="Generated Image")
