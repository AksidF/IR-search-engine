from collections import Counter

import os


class Loader:
    """
    Loader class that used to load the data for the stemmer, normalizer, and corrector.
    """

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = self.current_dir + "/../data"

    def _load_data(self, file_path) -> set[str]:
        with open(file_path) as f:
            content = f.read()
        return set(content.split())

    def load_root_words(self) -> set[str]:
        file_path = f"{self.data_dir}/root-words.txt"
        return self._load_data(file_path)

    def load_stop_words(self) -> set[str]:
        file_path = f"{self.data_dir}/stop-words.txt"
        return self._load_data(file_path)

    def load_words(self) -> set[str]:
        file_path = f"{self.data_dir}/words.txt"
        return self._load_data(file_path)

    def load_articles(self) -> Counter[str]:
        file_path = f"{self.data_dir}/word-articles.txt"
        with open(file_path) as f:
            content = f.read()
        list_content = content.split()
        return Counter(list_content)