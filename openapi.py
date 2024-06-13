import streamlit as st
import json
from openai import OpenAI

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("파일을 찾을 수 없습니다.")
        return None
    except json.JSONDecodeError:
        st.error("JSON 파일을 읽는 중 오류가 발생했습니다.")
        return None

data = load_data('book20.json')

if data:
    titles = data.get('title', [])
    introduces = data.get('introduce', [])
    tocs = data.get('toc', [])
    pub_reviews = data.get('pubReview', [])

    st.markdown(
        """
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }
        .stExpander {
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .stExpanderHeader {
            font-size: 18px;
            font-weight: bold;
        }
        .stExpanderContent {
            padding: 10px;
            font-size: 16px;
        }
        .header-title {
            text-align: center;
            font-size: 32px;
            color: #333;
            margin-bottom: 20px;
        }
        .header-subtitle {
            text-align: center;
            font-size: 24px;
            color: #666;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='header-title'>도서 검색 웹 애플리케이션</div>", unsafe_allow_html=True)

    api_key = st.text_input("OpenAI API Key:", placeholder="API 키를 입력하세요")
    if not api_key:
        st.warning("Please enter your OpenAI API key.")
        st.stop()

    client = OpenAI(api_key=api_key)

    def get_similar_books(input_text):
        vector_store = client.vector_stores.create(name="BOOK")

        with open('./book20_toc.json', "rb") as file_stream:
            client.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files=[file_stream]
            )

        assistant = client.assistants.create(
            instructions='당신은 사서입니다. 첨부 파일의 정보를 이용해 응답하세요.',
            model="gpt-4-turbo",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )

        thread = client.threads.create(
            messages=[{"role": "user", "content": f"입력 내용과 유사한 책을 첨부 파일에서 찾아서 title과 전체 내용을 요약해서 출력해\n출력 예: 제목:title\n-내용:...\n\n입력: {input_text}"}]
        )

        run = client.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
        thread_messages = client.threads.messages.list(thread.id, run_id=run.id)
        recommended_books = thread_messages.data[0].content[0].text.value

        client.threads.delete(thread.id)
        client.assistants.delete(assistant.id)
        client.vector_stores.delete(vector_store.id)
        
        return recommended_books

    st.markdown("<div class='header-subtitle'>도서 검색</div>", unsafe_allow_html=True)
    search_title = st.text_input("도서 제목을 입력하세요:", placeholder="예: The Great Gatsby")
    if st.button("검색하기"):
        if search_title:
            book = get_similar_books(search_title)
            st.write(book)
        else:
            st.warning("검색어를 입력하세요.")

    st.markdown("<div class='header-subtitle'>전체 도서 목록</div>", unsafe_allow_html=True)
    for i, title in enumerate(titles):
        with st.expander(title):
            st.markdown("<div class='stExpanderHeader'>소개</div>", unsafe_allow_html=True)
            st.write(introduces[i] if i < len(introduces) else "소개 정보가 없습니다.")
            st.markdown("<div class='stExpanderHeader'>목차</div>", unsafe_allow_html=True)
            st.write(tocs[i] if i < len(tocs) else "목차 정보가 없습니다.")
            st.markdown("<div class='stExpanderHeader'>출판사 리뷰</div>", unsafe_allow_html=True)
            st.write(pub_reviews[i] if i < len(pub_reviews) else "출판사 리뷰 정보가 없습니다.")
else:
    st.error("도서 데이터를 불러오는 중 문제가 발생했습니다.")



