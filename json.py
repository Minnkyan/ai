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

    st.title("도서 검색 웹 애플리케이션")
    
    key = search_title = st.text_input("key:")
    client = OpenAI(api_key=key)

    def get_similar_books(input):
    # 파일
        vector_store = client.beta.vector_stores.create(name="BOOK")

        path = './book20_toc.json'
        file_streams = open(path, "rb")

        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=[file_streams]
        )

        Prompt = "입력 내용과 유사한 책을 첨부 파일에서 찾아서 title과 전체 내용을 요약해서 출력해 \n출력 예: 제목:title \n -내용:...  \n\n입력: "

        assistant = client.beta.assistants.create(
            instructions= '당신은 사서입니다. 첨부 파일의 정보를 이용해 응답하세요.',
            model="gpt-4o",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search":{
                    "vector_store_ids": [vector_store.id]
                }
            }
        )

        #thread
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": Prompt + input,
                }
            ]
        )

        run = client.beta.threads.runs.create_and_poll( # 1초에 1회 호출 (분당 100회 제한)
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # message
        thread_messages = client.beta.threads.messages.list(thread.id, run_id=run.id)
        recommended_books = thread_messages.data[0].content[0].text.value
        # delete thread
        response = client.beta.threads.delete(thread.id)

        # delete assistant
        response = client.beta.assistants.delete(assistant.id)

        # delete vector store
        response = client.beta.vector_stores.delete(vector_store.id)
        
        return recommended_books

    st.header("도서 검색")
    search_title = st.text_input("도서 제목 혹은 도서의 내용을 입력하세요:")
    if st.button("검색하기"):
        book = get_similar_books(search_title)
        matching_titles = [title for title in titles if search_title.lower() in title.lower()]
        st.write(book)
        # if matching_titles:
        #     st.write(f"'{search_title}'에 대한 검색 결과:")
        #     for title in matching_titles:
        #         index = titles.index(title)
        #         st.subheader(title)
        #         st.write("**소개**")
        #         st.write(introduces[index] if index < len(introduces) else "소개 정보가 없습니다.")
        #         st.write("**목차**")
        #         st.write(tocs[index] if index < len(tocs) else "목차 정보가 없습니다.")
        #         st.write("**출판사 리뷰**")
        #         st.write(pub_reviews[index] if index < len(pub_reviews) else "출판사 리뷰 정보가 없습니다.")
        # else:
        #     st.write(f"'{search_title}'에 대한 검색 결과가 없습니다.")

    st.header("전체 도서 목록")
    for i, title in enumerate(titles):
        with st.expander(title):
            st.write("**소개**")
            st.write(introduces[i] if i < len(introduces) else "소개 정보가 없습니다.")
            st.write("**목차**")
            st.write(tocs[i] if i < len(tocs) else "목차 정보가 없습니다.")
            st.write("**출판사 리뷰**")
            st.write(pub_reviews[i] if i < len(pub_reviews) else "출판사 리뷰 정보가 없습니다.")
else:
    st.error("도서 데이터를 불러오는 중 문제가 발생했습니다.")
