from .cacher import Cacher
from .loader import Loader
from .logger import Logger
from typing import Optional

import string


class Corrector:
    """
    Corrector class that used to correct the spelling of the Balinese text language.

    Inspired by Peter Norvig's blog post: https://norvig.com/spell-correct.html
    """

    def __init__(
        self,
        document: Optional[dict[str, int]] = None,
        known_words: Optional[set[str]] = None,
    ):
        self.cache = Cacher()
        self.loader = Loader()
        self.logger = Logger().get_logger()
        self.document = (
            document if document is not None else self.loader.load_articles()
        )
        self.known_words = (
            known_words if known_words is not None else self.loader.load_words()
        )
        self.total_words_document = sum(self.document.values())

    def _edit_single(self, word) -> set[str]:
        "All edits that are one edit away from `word`."
        letters = string.ascii_lowercase
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def _edits(self, word, n) -> set[str]:
        "All edit that are `n` edits away from `word`."
        if n == 1:
            return self._edit_single(word)
        else:
            return set(
                e for e1 in self._edits(word, n - 1) for e in self._edit_single(e1)
            )

    def _is_known(self, word: str) -> bool:
        return word in self.known_words

    def _filter_known(self, words: set[str]) -> set[str]:
        return set(w for w in words if self._is_known(w))

    def _generate_candidates(self, word: str):
        return (
            self._filter_known(self._edits(word, 1))  # edit one distance
            or self._filter_known(self._edits(word, 2))  # edit two distance
            or set([word])  # no correction found, original word
        )

    def _get_probability(self, word):
        return self.document.get(word, 0) / self.total_words_document

    def correct_spelling(self, word: str) -> str:
        """
        Correct the spelling of the word.
        """
        if self._is_known(word):
            return word
        else:
            # word unknown, check on cache
            if self.cache.has(word):
                return self.cache.get(word)
            else:
                # do spelling correction
                try:
                    candidates = self._generate_candidates(word)
                    result = max(candidates, key=self._get_probability)

                    self.cache.set(word, result)
                    return result
                except Exception as e:
                    self.logger.error(
                        f"Failed to correct_spelling word: {word}, error: {e}"
                    )
                    return word
