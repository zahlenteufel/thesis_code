from prediction_text import PredictionText, UniversalSet
from itertools import chain


class PredictionTexts:

    def __init__(self, text_indexes, only_targets_in=UniversalSet()):
        self._prediction_texts = [
            PredictionText(i, only_targets_in) for i in text_indexes
        ]

    def lines(self):
        return self.flatten(t.lines() for t in self._prediction_texts)

    def words(self, filter_by=UniversalSet()):
        return flatten(t.words(filter_by=filter_by) for t in self._prediction_texts)

    def target_words(self, filter_by=UniversalSet()):
        return flatten(t.target_words(filter_by=filter_by) for t in self._prediction_texts)


def flatten(list_of_lists):
    return list(chain.from_iterable(list_of_lists))
