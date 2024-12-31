
# list doc example
# list_doc = [
#     ['saya', 'sedang', 'belajar', 'pemrosesan', 'bahasa', 'alami'],
#     ['saya', 'sedang', 'belajar', 'pemrosesan', 'bahasa', 'alami'],
#     ['saya', 'sedang', 'belajar', 'pemrosesan', 'bahasa', 'alami']
# ]
# output = {
#     'bahasa': [0, 1, 2],
#     'belajar': [0, 1, 2],
#     'pemrosesan': [0, 1, 2],
#     'saya': [0, 1, 2],
#     'sedang': [0, 1, 2],
# }
def inverted_indexing(list_doc : list[list[str]]) -> dict[str, list[int]]:
    inverted_index = {}
    for i in range(len(list_doc)):
        for word in list_doc[i]:
            if word not in inverted_index:
                inverted_index[word] = {i}
            else:
                inverted_index[word].add(i)
                
    return {key: sorted(inverted_index[key]) for key in sorted(inverted_index)}

