import csv
import json

from src.common.logger import logger
from src.load import search
from src.modules.preprocessing.spelling_correction.corrector import Corrector
from src.modules.preprocessing.text import text_preprocessing

import streamlit as st


@st.cache_data
def _load_corrector():
    indonesia_words = set()
    with open(
        "src/modules/preprocessing/spelling_correction/data/wordlist.txt",
        "r",
        encoding="utf-8",
    ) as file:
        content = file.read()
        for i in content.split():
            indonesia_words.add(i)

    with open(
        "src/modules/preprocessing/spelling_correction/data/word_freq.json", "r"
    ) as file:
        dataset_words = json.load(file)

    corrector = Corrector(dataset_words, indonesia_words)
    return corrector


def get_data(query: str):
    selected_index = search(query)
    result = [None] * len(selected_index)
    with open("data/IR_dataset.tsv", mode="r", encoding="utf-8") as file:
        tsv_reader = csv.DictReader(file, delimiter="\t")

        for idx, row in enumerate(tsv_reader):
            if idx in selected_index:
                rank = selected_index.index(idx)
                result[rank] = row

    return result


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


def show_result(query: str):
    corrector = _load_corrector()
    correct_query = []
    for word in query.lower().split():
        correct_query.append(corrector.correct_spelling(word))

    correct_query = " ".join(correct_query)
    preprocess_query = text_preprocessing(correct_query, stem=True)
    result_query = " ".join(preprocess_query)

    logger.info(f"Corrected query: {correct_query}")
    logger.info(f"Preprocessed query: {result_query}")

    selected_data = get_data(result_query)
    st.divider()
    st.info(
        f"""
            Showing {len(selected_data)} result
            for *{result_query}*""",
        icon=":material/info:",
    )
    if len(selected_data) == 0:
        st.warning(
            "No result found. Please try another query or check your spelling.",
            icon=":material/warning:",
        )

    search_cols = st.columns(3, gap="large")

    for i in range(0, len(selected_data)):
        with search_cols[i % 3]:
            st.markdown(f"**{selected_data[i]["title"]}**")
            st.caption(selected_data[i]["url"])
            st.markdown(f"{_split_content(selected_data[i]["content"])}")
            st.divider()
