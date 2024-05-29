import streamlit as st
import openai

# API 키 입력을 받는 함수
def get_api_key():
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    if api_key:
        st.session_state["api_key"] = api_key
    return st.session_state.get("api_key", "")

# 캐시된 함수: 사용자 질문에 대한 응답을 캐싱
@st.cache_data
def get_gpt_response(api_key, user_input):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("GPT-3.5-turbo Response Generator")
    
    # API 키를 입력받고 세션 상태에 저장
    api_key = get_api_key()
    if not api_key:
        st.warning("Please enter your OpenAI API Key.")
        return
    
    # 사용자 질문 입력 받기
    user_input = st.text_input("Enter your question:")
    
    # 응답 생성 버튼
    if st.button("Get Response"):
        if user_input:
            try:
                # 캐시된 함수 호출
                response = get_gpt_response(api_key, user_input)
                st.text_area("Response from GPT-3.5-turbo:", response, height=200)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
