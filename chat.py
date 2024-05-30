!pip install openai
import streamlit as st
from openai import APIException, openai
import threading

class ChatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.messages = []

    def run(self):
        try:
            self.assistant = openai.ChatCompletion.create(
                model="gpt-4o", messages=self.messages)
        except APIException as e:
            st.error(f"An error occurred: {e}")

    def append_message(self, role, content):
        self.messages.append({"role": role, "content": content})

def clear_thread(thread):
    if thread is not None and thread.is_alive():
        thread.assistant.delete()
        thread.join()
        st.success("Chat cleared and new thread started.")

def main():
    st.title("OpenAI Assistant Chat")

    thread = None

    if st.button("Start Chat"):
        thread = ChatThread()
        thread.start()

    if thread is not None and thread.is_alive():
        user_input = st.text_input("You:", key="user_input")
        if st.button("Send"):
            if user_input:
                thread.append_message("user", user_input)
                st.write("You:", user_input)
                st.write("Assistant:", thread.assistant.messages[-1]["content"])

    if st.button("Clear Chat"):
        clear_thread(thread)

    if st.button("Exit Chat"):
        clear_thread(thread)
        st.stop()

if __name__ == "__main__":
    main()
  
