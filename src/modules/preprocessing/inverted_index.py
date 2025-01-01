import csv
import json
import os
from .text import text_preprocessing
from .tfidf import TFIDF

import numpy as np


def inverted_indexing(list_doc: list[list[str]]) -> dict[str, list[int]]:
    inverted_index = {}
    for i in range(len(list_doc)):
        for word in list_doc[i]:
            if word not in inverted_index:
                inverted_index[word] = {i}
            else:
                inverted_index[word].add(i)

    return {key: sorted(inverted_index[key]) for key in sorted(inverted_index)}


def build_inverted_index():
    file_path = os.path.join(os.path.dirname(__file__))

    data = []

    with open(
        f"{file_path}/../../../data/IR_dataset.tsv", "r", newline="", encoding="utf-8"
    ) as file:
        tsv_reader = csv.reader(file, delimiter="\t")

        # Iterasi setiap baris
        for row in tsv_reader:
            data.append(row[2])

    data = data[1:]  # skip header

    preprocessed_data = []
    tfidf_data = []
    for doc in data:
        clean_data = text_preprocessing(doc)
        preprocessed_data.append(clean_data)
        tfidf_data.append(" ".join(clean_data))

    tf_idf = TFIDF()
    vect_data = tf_idf.fit_transform(tfidf_data)

    np.save(f"{file_path}/../../../compressed/vect_data.npy", vect_data)

    inverted_index_data = inverted_indexing(preprocessed_data)

    assert np.array_equal(tf_idf.word_to_index.keys(), inverted_index_data.keys())

    tfidf_config = {
        "word_counter": tf_idf.word_counter,
        "index_to_word": tf_idf.index_to_word,
        "word_to_index": tf_idf.word_to_index,
        "document_frequency": tf_idf.document_frequency,
        "n_docs": tf_idf.n_docs,
        "n_vocab": tf_idf.n_vocab,
    }

    with open(f"{file_path}/../../../compressed/tfidf_config.json", "w") as file:
        json.dump(tfidf_config, file)

    return inverted_index_data
