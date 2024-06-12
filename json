pip install streamlit
import streamlit as st
import json

with open('book_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

titles = data['title']
introduces = data['introduce']
tocs = data['toc']
pub_reviews = data['pubReview']

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
            st.write(introduces[index])
            st.write("**목차**")
            st.write(tocs[index])
            st.write("**출판사 리뷰**")
            st.write(pub_reviews[index])
    else:
        st.write(f"'{search_title}'에 대한 검색 결과가 없습니다.")

st.header("전체 도서 목록")
for i, title in enumerate(titles):
    with st.expander(title):
        st.write("**소개**")
        st.write(introduces[i])
        st.write("**목차**")
        st.write(tocs[i])
        st.write("**출판사 리뷰**")
        st.write(pub_reviews[i])
