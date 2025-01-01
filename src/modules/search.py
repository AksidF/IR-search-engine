from collections import Counter
import numpy as np

from src.common.cache import cacher
from src.common.logger import logger
from src.modules.cosine_similarity import cosine_similarity

import numpy as np


def _match_documents(
    query: list[str],
    index: dict[str, list[int]],
    threshold: float = 1,
):
    selected_idx = []
    for term in query:
        if term in index:
            selected_idx.append(index[term])
        else:
            selected_idx.append([])
    # bcs each item on posting list is unique, we can flatten it
    flatten = [item for posting in selected_idx for item in posting]
    counter = Counter(flatten)
    threshold = int(len(query) * threshold)
    result = [key for key, value in counter.items() if value >= threshold]
    return result


def _match_similarity_documents(query: list[str], top_n=5):
    sentence = " ".join(query)
    sentence_vector = cacher.get("__tfidf__").transform([sentence])
    if np.all(sentence_vector == 0):
        return []
    cosine_similarities = cosine_similarity(
        sentence_vector, cacher.get("__docs_vector__")
    )[0]
    top_idx = np.argsort(cosine_similarities)[-top_n:][::-1]
    return top_idx.tolist()


def search_documents(
    query: list[str],
    index: dict[str, list[int]],
):
    # match 100%
    match_all = _match_documents(query, index, 1)
    logger.info(f"Match all: {match_all}")

    # match 75%
    match_75 = _match_documents(query, index, 0.75)
    logger.info(f"Match 75%: {match_75}")

    # match bi-gram
    match_bi_gram = []
    if len(query) >= 3:
        n_gram = 2
        for i in range(len(query) - n_gram + 1):
            bi_gram = query[i : i + n_gram]
            match_bi_gram.extend(_match_documents(bi_gram, index, 1))
    logger.info(f"Match bi-gram: {match_bi_gram}")

    # cosine similarity
    match_similarity = _match_similarity_documents(query)
    logger.info(f"Match similarity: {match_similarity}")

    all_result = (
        set(match_all) | set(match_75) | set(match_bi_gram) | set(match_similarity)
    )

    return all_result


def rank_documents(query: str, list_doc_id):
    if len(list_doc_id) == 0:
        return []
    docs_vector = cacher.get("__docs_vector__")
    doc_list = docs_vector[list_doc_id, :]

    sentence_vector = cacher.get("__tfidf__").transform([query])
    if np.all(sentence_vector == 0):
        return list_doc_id
    cosine_similarities = cosine_similarity(sentence_vector, doc_list)[0]

    sorted_doc_ids = [list_doc_id[i] for i in np.argsort(cosine_similarities)[::-1]]
    logger.info(f"Sorted doc ids: {sorted_doc_ids}")
    return sorted_doc_ids
