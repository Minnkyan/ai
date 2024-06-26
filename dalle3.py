import streamlit as st
from openai import OpenAI
from PIL import Image
import requests

# Streamlit 페이지 설정
st.set_page_config(page_title="Image Generator with Dall-E", layout="wide")

# Dall-E 이미지 생성을 위한 함수
@st.cache(suppress_st_warning=True, allow_output_mutation=True, hash_funcs={OpenAI: id})
def generate_image(prompt, api_key):
    client = OpenAI(api_key=api_key)
    try:
        response = client.Completion.create(
            model="image-dalle-2",  # 모델 이름은 OpenAI의 최신 문서를 참조하세요.
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.choices[0].url
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        return image
    except Exception as e:
        st.error(f"Failed to generate image: {str(e)}")
        return None

# API 키 입력
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# 사용자 프롬프트 입력
if "user_prompt" not in st.session_state:
    st.session_state.user_prompt = ""

prompt = st.text_input("Enter your prompt for the image", value=st.session_state.user_prompt)
st.session_state.user_prompt = prompt

# 이미지 생성 및 표시
if prompt:
    if not api_key:
        st.warning("Please enter the API key to generate an image.")
    else:
        image = generate_image(prompt, api_key=api_key)
        if image:
            st.image(image, caption="Generated Image")

# 코드 설명:
# 1. 세션 상태를 사용하여 사용자의 프롬프트 입력을 저장하고, 다른 페이지로 이동한 후에도 유지합니다.
# 2. `@st.cache` 데코레이터를 사용하여 동일한 프롬프트에 대한 API 호출을 캐시하여 API 호출을 최소화합니다.
# 3. 예외 처리를 통해 API 호출 실패 시 사용자에게 적절한 오류 메시지를 표시합니다.
