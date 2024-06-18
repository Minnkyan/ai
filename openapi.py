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

data = load_data('book100.json')

if data:
    titles = data.get('title', [])
    introduces = data.get('introduce', [])
    tocs = data.get('toc', [])

    st.title("도서 검색 웹 애플리케이션")
    
    key = search_title = st.text_input("key:")
    client = OpenAI(api_key=key)

    def get_similar_books(input):
        # 파일
        vector_store = client.beta.vector_stores.create(name="BOOK")
    
        file_streams = []
        for i in range(50):
            file_streams.append(open(f"books/book{i+1}.json", "rb"))
    
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams
        )
    
        Prompt = f'''
        다음 작업을 수행하시오.
        1. 첨부 파일에서 세 개의 역따옴표로 구분된 입력 내용과 연관이 있는 내용이 담긴 책을 찾는다.
        2. 1에서 찾은 책의 title을 csv형식으로 구분자는 '\\n'으로 하고 출력하세요.
        
        출력시 출처는 포함하지 마세요.
        
        다음 형식으로 출력하시오.
        title1
        title2
        title3
        
    
    
        입력:
        ```{input}```
        '''
        
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
        # 12초
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
    
        # delete files
        response = client.files.list(purpose="assistants")
        for file in response.data:
            try:
                client.files.delete(file.id)
            except:
                pass
        
        return recommended_books

    # 사이드바 메뉴
menu = st.sidebar.radio("메뉴를 선택하세요", ["도서 검색", "사용법"])

if menu == "도서 검색":
    st.header("도서 검색")  
    search_title = st.text_input("도서 제목 혹은 도서의 내용을 입력하세요:")

    if st.button("검색하기"):
        with st.spinner('검색 중 ...'):
            book = get_similar_books(search_title)
        books = book.split('\n')

        st.write(f"'{search_title}'에 대한 검색 결과:")
        
        books = list(set(books) & set(titles))
        if books != []:
            for book in books:
                index = titles.index(book)
                with st.expander(book):
                    st.write("**소개**")
                    st.write(introduces[index] if introduces[index] != '' else "소개 정보가 없습니다.")
                    st.write("**목차**")
                    st.write(tocs[index] if tocs[index] != '' else "목차 정보가 없습니다.")
        else:
            st.write('검색 결과가 없습니다. 다시 검색해주세요.')

elif menu == "사용법":
    st.header("사용법 안내")
    st.write("""
        ### 도서 검색 웹 애플리케이션 사용법

        1. **OpenAI API Key 입력**: 애플리케이션을 사용하기 위해 OpenAI API Key를 입력하세요.
    """)
    # 이미지 삽입
    st.image("image.png")
    st.write("""
        2. **도서 검색**:
            - 사이드바에서 '도서 검색' 메뉴를 선택하세요.
            """)
    st.image("image2.png")
    st.write("""
            - 검색하고자 하는 도서 제목 혹은 도서의 내용을 입력하고 '검색하기' 버튼을 클릭하세요.
            """)
    st.image("image3.png")
    st.write("""
            - 검색 결과로 관련 도서 목록이 표시됩니다.
            """)
    st.image("image4.png")
    st.write("""
            - 각 도서의 제목을 클릭하면 도서의 소개 및 목차 정보를 확인할 수 있습니다.
            """)
    st.image("image5.png")
            

