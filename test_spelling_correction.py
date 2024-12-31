import sys
import os
import json
from module_spelling_correction.corrector import Corrector


current_path = os.path.dirname(os.path.realpath(__file__))

indonesia_words = set()
with open(f"{current_path}/module_spelling_correction/data/wordlist.txt", 'r', encoding='utf-8') as file:
    content = file.read()
    for i in content.split():
        indonesia_words.add(i)
        
with open(f"{current_path}/module_spelling_correction/data/word_freq.json", 'r') as file:
    dataset_words = json.load(file)


corrector = Corrector(
    document=dataset_words, 
    known_words=indonesia_words
    )


print(corrector.correct_spelling('rabot'))  # Output: robot