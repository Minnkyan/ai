from openai import OpenAI
import streamlit as st

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


def takeInput():
    # Title
    st.title('Make me an Image')
    # Ask for the API key
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

    # Ask for the model choice
    model_choice = st.selectbox(
        "Which Dall E model would you like to use? ",
        ("DALL·E 3", "DALL·E 2"),
        index=None,
        key="model_choice",
        placeholder="Select DALL·E model",
    )
    # Display user choice
    st.write('You selected:', model_choice)

    # Logic if no model is selected
    if model_choice == "DALL·E 3":
        model_choice = "dall-e-3"
    else:
        model_choice = "dall-e-2"

    # Takes the user prompt

    prompt = st.text_input("Enter a prompt:", key="user_prompt_input")

    return model_choice, prompt, api_key

import streamlit as st
import requests
from io import BytesIO
from PIL import Image

def generateImage(client, model_choice, prompt):
    if st.button("Generate Image"):
        # create the image generation request
        response = client.images.generate(
            model=model_choice,
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1 #This can be modified but currently DALL.E 3 only supports 1
        )
        image_url = response.data[0].url
        print("Generated Image URL:", image_url)

        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        # Display the image
        st.image(img)








