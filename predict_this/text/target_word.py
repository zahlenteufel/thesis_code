from word import Word
from word import to_ascii
from numpy import mean
from numpy import log10


class TargetWord(Word):

    def __init__(self, word, lemma, category_code, text_index, word_index, context, completed_words):
        Word.__init__(self, word, lemma, category_code, text_index, word_index)
        self._context = context
        self._completed_words = map(to_ascii, completed_words)

    def cloze_prob(self):
        "empirical frequency, normalized to avoid probabilities 0 and 1"
        return self._cloze_prob(self.in_ascii())

    def _cloze_prob(self, word):
        count = self._completed_words.count(word)
        n = len(self._completed_words)
        if count == 0:
            return 1 / float(n + 1)
        elif count == n:
            return n / float(n + 1)
        else:
            return count / float(n + 1)

    def context(self):
        return self._context

    def is_target(self):
        return True

    @staticmethod
    def from_csv_row(row, current_line):
        if row["completed_words"]:
            return TargetWord(
                word=row["word"],
                lemma=row["lemma"],
                category_code=row["tag"],
                text_index=int(row["text_index"]),
                word_index=int(row["word_index"]),
                context=current_line[:],
                completed_words=parse_completed_words(row["completed_words"]),
            )
        else:
            return Word(
                word=row["word"],
                lemma=row["lemma"],
                category_code=row["tag"],
                text_index=int(row["text_index"]),
                word_index=int(row["word_index"]),
            )


def parse_completed_words(completed_words_string):
    return sorted(filter(None, completed_words_string.replace(u"[", u"").replace(u"]", u"").split(u" ")))
