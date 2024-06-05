from openai import OpenAI
import streamlit as st
from dall_e         import map_pixels, unmap_pixels
from dall_e.encoder import DALLEncoder

encoder = DALLEncoder()

def generate_image(text):
    vector = encoder.encode_text(text)
    image = encoder.decode(vector)
    return image

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("챗봇")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API 키를 입력하세요.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="dall-e-3", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

def second_page():
    st.title('Second Page')

    user_input = st.text_input('Enter text for image generation:')

    if st.button('Generate Image'):
        image = generate_image(user_input)
        st.image(image, caption='Generated Image', use_column_width=True)

def main():
    page = st.sidebar.radio("Go to", ["First Page", "Second Page"])

    if page == "First Page":
        first_page()
    elif page == "Second Page":
        second_page()

if __name__ == '__main__':
    main()





