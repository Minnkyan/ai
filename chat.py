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








