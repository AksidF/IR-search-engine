from modules.dictionary import parse_string_to_list
from modules.vb_decode import vb_decode_line_to_doc_ids

def load_dictionary(file_path):
    """
    Load the dictionary string from a file and parse it into a list of terms.

    Args:
        file_path (str): Path to the dictionary string file.

    Returns:
        list[str]: List of terms.
    """
    with open(file_path, 'r') as file:
        dictionary_string = file.read().strip()
    terms = parse_string_to_list(dictionary_string)
    print(f"Loaded and parsed dictionary from {file_path}.")
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
            print(f"Decoded VB-encoded indices for line {line_index}.")
        except IndexError as e:
            print(f"Error: {e}")
            decoded_indices[line_index] = None
    return decoded_indices

# Example usage, delete later
if __name__ == "__main__":
    dictionary_file = "compressed/dictionary_string.txt"
    vb_encoded_file = "compressed/vb_encoded.txt"

    # Load dictionary
    terms = load_dictionary(dictionary_file)
    print("Terms:", terms)

    # Load VB-encoded indices for multiple terms
    term_to_lookups = ["Abidin", "Abilah", "Abing"]
    line_indices = [terms.index(term) for term in term_to_lookups if term in terms]
    decoded_doc_ids = load_vb_encoded_indices(vb_encoded_file, line_indices)

    # Map terms to their decoded document IDs
    term_doc_ids_mapping = {
        terms[line_index]: doc_ids for line_index, doc_ids in decoded_doc_ids.items()
    }
    print("Term to Document IDs Mapping:", term_doc_ids_mapping)
