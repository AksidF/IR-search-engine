import pandas as pd
from tfidf import TFIDF
import numpy as np

df = pd.read_excel("IR-search-engine/data/IR_dataset.xlsx")

INV_INDEX = {}
for idx, row in df.iterrows():
    splitted_content = row["content"].split()
    for term in splitted_content:
        if term not in INV_INDEX:
            INV_INDEX[term] = set()
        INV_INDEX[term].add(idx)

for key in INV_INDEX.keys():
    INV_INDEX[key] = list(INV_INDEX[key])

tfidf = TFIDF()
content_list = (df["content"].tolist())

VECT_CONTENT = tfidf.fit_transform(content_list)
print(INV_INDEX)