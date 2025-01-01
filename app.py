import streamlit as st

home_page = st.Page("src/views/home.py", title="Home Page", icon=":material/home:")

pg = st.navigation([home_page])
pg.run()
