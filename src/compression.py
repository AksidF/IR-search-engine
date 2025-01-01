from modules.dictionary import convert_list_to_str
from modules.vb_encoding import save_vb_encoded_bits_to_file_multiline
from modules.preprocessing.inverted_index import build_inverted_index

def compress_inverted_index(inverted_index):
    """
    Compress an inverted index by saving the dictionary string and VB-encoded indices to files.

    Args:
        inverted_index (dict): Inverted index with terms as keys and lists of doc_ids as values.
    """

    dictionary_file = "compressed/dictionary_string.txt"
    vb_encoded_file = "compressed/vb_encoded.txt"

    #Convert terms to a dictionary string format
    terms = list(inverted_index.keys())
    dictionary_string = convert_list_to_str(terms)

    with open(dictionary_file, 'w') as file:
        file.write(dictionary_string)
    print(f"Dictionary string saved to {dictionary_file}.")

    # Index lists for VB encoding
    index_lists = list(inverted_index.values())
    
    save_vb_encoded_bits_to_file_multiline(index_lists, vb_encoded_file)
    print(f"VB encoded data saved to {vb_encoded_file}. Compression completed.")

# Example usage, delete later
if __name__ == "__main__":
    inverted_index = build_inverted_index()
    compress_inverted_index(inverted_index)
