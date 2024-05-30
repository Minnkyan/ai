from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

st.title("웹 앱")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "질문을 입력하세요."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("OpenAI API 키를 입력하세요.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

st.sidebar.markdown("[2번째 페이지로 이동](./)")

st.title("DALL-E 이미지 생성기")
prompt = st.text_input("프롬프트를 입력하세요:", st.session_state['prompt'])

if st.button("이미지 생성"):
    if prompt:
        st.session_state['prompt'] = prompt
        prompt_hash = get_prompt_hash(prompt)
        
        if prompt_hash in st.session_state['image_cache']:
            image_url = st.session_state['image_cache'][prompt_hash]
        else:
            image_url = generate_image(prompt)
            st.session_state['image_cache'][prompt_hash] = image_url

        st.image(image_url, caption=prompt)
