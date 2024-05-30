import streamlit as st

if "messages" not in st.session_state: 
    st.session_state.messages = []

for msg in st.session_state.messages: 
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

prompt = st.text_input("What is up?")
if prompt: 
    st.chat_message("user").markdown(prompt) 
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    response = f"Echo: {prompt}" 
    with st.chat_message("assistant"): 
        st.markdown(response) 
        st.session_state.messages.append({"role": "assistant", "content": response})
  
