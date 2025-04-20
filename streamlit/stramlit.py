import streamlit as st


search_page = st.Page("search.py", title="검색", icon=":material/add_circle:")
keyword_page = st.Page("keyword.py", title="키워드", icon=":material/add_circle:")
home_page = st.Page("home.py", title="홈", icon=":house:")

pg = st.navigation([home_page, search_page, keyword_page])
pg.run()
