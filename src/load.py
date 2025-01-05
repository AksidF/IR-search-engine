import sys
import numpy as np
import json

from src.common.cache import cacher
from src.common.logger import logger
from src.modules.dictionary import (
    parse_string_to_list,
    generate_blocking_tree,
    search_bloking_tree,
)
from src.modules.preprocessing.text import text_preprocessing
from src.modules.preprocessing.tfidf import TFIDF
from src.modules.search import search_documents, rank_documents
from src.modules.vb_decode import vb_decode_line_to_doc_ids
from src.utils.splitter import load_chunk_np

sys.setrecursionlimit(5_000)


def load_dictionary(file_path):
    """
    Load the dictionary string from a file and parse it into a list of terms.

    Args:
        file_path (str): Path to the dictionary string file.

    Returns:
        list[str]: List of terms.
    """
    with open(file_path, "r") as file:
        dictionary_string = file.read().strip()
    terms = parse_string_to_list(dictionary_string)
    logger.info(f"Loaded and parsed dictionary from {file_path}.")
    return terms


def load_vb_encoded_indices(vb_encoded_file, line_indices):
    """
    Load and decode the VB-encoded indices for multiple lines in the file.

    Args:
        vb_encoded_file (str): Path to the VB-encoded indices file.
        line_indices (list[int]): List of line indices to decode.

    Returns:
        dict[int, list[int]]: A dictionary mapping line indices to decoded document IDs.
    """
    decoded_indices = {}
    for line_index in line_indices:
        try:
            doc_ids = vb_decode_line_to_doc_ids(vb_encoded_file, line_index)
            decoded_indices[line_index] = doc_ids
            logger.info(f"Decoded VB-encoded indices for line {line_index}.")
        except IndexError as e:
            logger.error(f"Error: {e}")
            decoded_indices[line_index] = None
    return decoded_indices


def load_tfidf_config(file_path):
    with open(file_path, "r") as file:
        config = json.load(file)
    return config


def search(query: str) -> list[int]:
    preprocessed_query = text_preprocessing(query)

    dictionary_file = "compressed/dictionary_string.txt"
    vb_encoded_file = "compressed/vb_encoded.txt"

    tfidf_config = load_tfidf_config("compressed/tfidf_config.json")
    tfidf_config["index_to_word"] = {
        int(k): v for k, v in tfidf_config["index_to_word"].items()
    }
    tfidf = TFIDF(**tfidf_config)
    cacher.set("__tfidf__", tfidf)

    docs_vector = load_chunk_np("compressed/chunks")
    # docs_vector = np.load("compressed/vect_data.npy")

    cacher.set("__docs_vector__", docs_vector)

    terms = load_dictionary(dictionary_file)

    root, graph = generate_blocking_tree(terms, terms)

    inv_index_query = {}
    for q in preprocessed_query:
        result = search_bloking_tree(q, root)
        if result is not None:
            inv_index_query.update({result.index: q})

    decoded_doc_ids = load_vb_encoded_indices(vb_encoded_file, inv_index_query.keys())

    result_inv_index = {inv_index_query.get(k): v for k, v in decoded_doc_ids.items()}

    search_results = list(search_documents(preprocessed_query, result_inv_index))
    ranked_results = rank_documents(query, search_results)

    return ranked_results
