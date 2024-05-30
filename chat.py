import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO

st.title("OpenAI API 웹 앱")
st.write("GPT-3.5-turbo 및 DALL-E를 사용하여 텍스트와 이미지를 생성합니다.")

api_key = st.text_input("OpenAI API Key를 입력하세요:", type="password")

if api_key:
    openai.api_key = api_key

    user_prompt = st.text_input("프롬프트를 입력하세요:")

    if user_prompt:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )

        gpt_response = response['choices'][0]['message']['content']
        st.subheader("GPT-3.5-turbo의 응답:")
        st.write(gpt_response)

        st.subheader("DALL-E로 생성한 이미지:")

        try:
            dalle_response = openai.Image.create(
                prompt=user_prompt,
                n=1,
                size="512x512"
            )
            image_url = dalle_response['data'][0]['url']
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption='DALL-E 이미지', use_column_width=True)
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
