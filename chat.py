from openai import OpenAI
import streamlit as st
from PIL import Image
import io

# Streamlit 페이지 설정
st.set_page_config(page_title="Chatbot and Image Generator", layout="wide")

# Dall-E 이미지 생성을 위한 함수
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def generate_image(prompt, api_key):
    client = OpenAI(api_key=api_key)
    response = client.images.generate(prompt=prompt, n=1, size="1024x1024")
    image_data = response['data'][0]['url']
    image = Image.open(io.BytesIO(image_data))
    return image

# 페이지 선택
page = st.sidebar.selectbox("Choose a page", ["Chatbot", "Image Generator"])

# Chatbot 페이지
if page == "Chatbot":
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    st.title("💬 Chatbot")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("키를 입력하세요.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

# 이미지 생성 페이지
elif page == "Image Generator":
    with st.sidebar:
        openai_api_key = st.text_input("Dall-E OpenAI API Key", key="dalle_api_key", type="password")
    st.title("🖼️ Image Generator")
    prompt = st.text_input("Enter a prompt for the image")
    if prompt:
        if not openai_api_key:
            st.info("Please enter the API key.")
            st.stop()

        # 프롬프트와 API 키로 이미지 생성
        image = generate_image(prompt, openai_api_key)
        st.image(image, caption="Generated Image")

