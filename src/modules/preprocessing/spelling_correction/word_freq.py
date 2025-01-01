# %%
import csv as tsv
import re


# %%
file_path = "IR_dataset.tsv"

# %%
data = []

# %%
# Membaca file TSV
with open(file_path, "r", newline="", encoding="utf-8") as file:
    tsv_reader = tsv.reader(file, delimiter="\t")

    # Iterasi setiap baris
    for row in tsv_reader:
        data.append(row[2])

# %%
cleaned_data = []

# %%
for i in range(len(data)):
    if i == 0:
        continue
    temp = data[i].lower()
    temp = re.findall(r"[a-zA-Z]+", temp)
    cleaned_data += temp

# %%
import collections

# Menghitung frekuensi kata
word_freq = collections.Counter(cleaned_data)


# %%
word_freq

# %%
import json

# %%
with open("word_freq.json", "w") as file:
    json.dump(word_freq, file)
