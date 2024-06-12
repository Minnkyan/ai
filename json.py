import streamlit as st
import json

# JSON 파일을 읽어오는 함수, 오류 처리 포함
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

data = load_data(PASS)

if data:
    titles = data.get('title', [])
    introduces = data.get('introduce', [])
    tocs = data.get('toc', [])
    pub_reviews = data.get('pubReview', [])

    st.title("도서 검색 웹 애플리케이션")

    st.header("도서 검색")
    search_title = st.text_input("도서 제목을 입력하세요:")

    if search_title:
        matching_titles = [title for title in titles if search_title.lower() in title.lower()]
        if matching_titles:
            st.write(f"'{search_title}'에 대한 검색 결과:")
            for title in matching_titles:
                index = titles.index(title)
                st.subheader(title)
                st.write("**소개**")
                st.write(introduces[index] if index < len(introduces) else "소개 정보가 없습니다.")
                st.write("**목차**")
                st.write(tocs[index] if index < len(tocs) else "목차 정보가 없습니다.")
                st.write("**출판사 리뷰**")
                st.write(pub_reviews[index] if index < len(pub_reviews) else "출판사 리뷰 정보가 없습니다.")
        else:
            st.write(f"'{search_title}'에 대한 검색 결과가 없습니다.")

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
