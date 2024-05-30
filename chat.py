import streamlit as st
import threading
from openai import OpenAI

# Placeholder for thread reference
global thread_reference
thread_reference = None

def run_thread(prompt, openai_api_key):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

# Clear button action
def clear_thread():
    global thread_reference
    if thread_reference is not None:
        if thread_reference.is_alive():
            # Thread termination logic can go here if required
            pass
    st.session_state.messages = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]
    st.experimental_rerun()

# Exit button action
def exit_app():
    global thread_reference
    if thread_reference is not None:
        if thread_reference.is_alive():
            # Thread termination logic can go here if required
            pass
        thread_reference = None
    st.session_state.messages = []
    st.stop()

# Streamlit app layout
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if st.button("Clear"):
        clear_thread()
    if st.button("Exit"):
        exit_app()

st.title("💬 Chatbot(챗봇)")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    global thread_reference
    thread_reference = threading.Thread(target=run_thread, args=(prompt, openai_api_key))
    thread_reference.start()
