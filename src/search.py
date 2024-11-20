import random

import pandas as pd
import streamlit as st


@st.cache_data
def get_data() -> pd.DataFrame:
    df = pd.read_excel("data/IR_dataset.xlsx")
    return df


def _split_content(text: str) -> str:
    splitted = text.split()
    char_count = 0
    result = ""
    for word in splitted:
        char_count += len(word)
        result += word + " "
        if char_count > 100:
            break
    result += "..."
    return result


def show_result():
    data = get_data().to_dict(orient="records")
    selected_data = []
    for i in data:
        if random.choice([True, False]):
            selected_data.append(i)
        if len(selected_data) > random.randint(10, 20):
            if random.choice([True, False]):
                break

    st.divider()
    st.info(f"Showing {len(selected_data)} result", icon=":material/info:")

    search_cols = st.columns(3, gap="large")

    for i in range(0, len(selected_data)):
        with search_cols[i % 3]:
            st.markdown(f"**{selected_data[i]['title']}**")
            st.caption(selected_data[i]["url"])
            st.markdown(f"{_split_content(selected_data[i]['content'])}")
            st.divider()
