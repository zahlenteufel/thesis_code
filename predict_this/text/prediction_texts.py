from prediction_text import PredictionText
from itertools import chain


class PredictionTexts:

    def __init__(self, text_indexes):
        self._prediction_texts = map(PredictionText, text_indexes)
        self._lines = flatten(t.lines() for t in self._prediction_texts)

    def lines(self):
        return self._lines

    def target_words(self):
        return flatten(t.target_words() for t in self._prediction_texts)


def flatten(list_of_lists):
    return list(chain.from_iterable(list_of_lists))
