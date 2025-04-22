import streamlit as st


search_page = st.Page("search.py", title="검색")
keyword_page = st.Page("keyword.py", title="키워드")
home_page = st.Page("home.py", title="홈")
llm_page = st.Page("llm.py", title="LLM")

pg = st.navigation([home_page, search_page, keyword_page, llm_page])
pg.run()
