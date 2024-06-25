import streamlit as st
import openai
from openai import OpenAI

# API Key 입력 받기
key = search_title = st.text_input("key:")
client = OpenAI(api_key=key)

# 페이지 설정
page = st.sidebar.selectbox("Select a page", ["Chat", "Generate Image"])

# 캐시된 함수 정의
@st.cache_data
def get_openai_response(key, prompt):
    api_key = key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

@st.cache_data
def generate_dalle_image(api_key, prompt):
    openai.api_key = api_key
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

if page == "Chat":
    st.title("Chat with GPT-3.5-turbo")

    # 메모리 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 저장한 메시지 사용자/응답 구분해서 보여주기
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["content"])

    # 사용자 입력과 LLM 응답
    if prompt := st.chat_input("Enter your message:"):
        # 사용자 메시지 보여주기
        st.chat_message("user").markdown(prompt)
        
        # 메모리에 사용자 메시지 저장
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # LLM 응답 생성
        response = get_openai_response(st.session_state.api_key, prompt)
        
        # LLM 응답 보여주기
        st.chat_message("assistant").markdown(response)
        
        # 메모리에 LLM 응답 저장
        st.session_state.messages.append({"role": "assistant", "content": response})

elif page == "Generate Image":
    st.title("Generate Images with DALL-E")

    # 메모리 초기화
    if "image_prompt" not in st.session_state:
        st.session_state.image_prompt = ""

    # 사용자 프롬프트 입력 받기
    image_prompt = st.text_input("Enter a prompt for the image")

    if image_prompt:
        # 메모리에 사용자 프롬프트 저장
        st.session_state.image_prompt = image_prompt
        
        # DALL-E 이미지 생성
        image_url = generate_dalle_image(st.session_state.api_key, image_prompt)
        
        # 생성된 이미지 보여주기
        st.image(image_url, caption=image_prompt)
