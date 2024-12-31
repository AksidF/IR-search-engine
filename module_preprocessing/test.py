import csv
from preprocessing import text_preprocessing
from inverted_indexing import inverted_indexing
import os

file_path = os.path.join(os.path.dirname(__file__))

data = []

with open(f"{file_path}/../data/IR_dataset.tsv", 'r', newline='', encoding='utf-8') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    
    # Iterasi setiap baris
    for row in tsv_reader:
        data.append(row[2])

data = data[1:]

preprocessed_data = []
for doc in data:
    preprocessed_data.append(text_preprocessing(doc))
    
inverted_index_data = inverted_indexing(preprocessed_data)

for key, value in inverted_index_data.items():
    print(f"{key} : {value}")