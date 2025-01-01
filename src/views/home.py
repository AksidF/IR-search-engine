import streamlit as st
from src.views.search import show_result

st.header("TechScout")
st.markdown(
    """
        TechScout is an advanced information retrieval system designed to simplify the search for technology-related articles and data.
        With its intelligent algorithms and user-friendly interface.
        TechScout ensures fast, accurate, and relevant results to empower your journey in technology exploration.
    """
)

col_text, col_search = st.columns([0.90, 0.10], vertical_alignment="bottom")
with col_text:
    title = st.text_input("Search", placeholder="Search for technology articles...")
with col_search:
    btn = st.button(label="", icon=":material/search:")

if btn or title:
    show_result(title)
