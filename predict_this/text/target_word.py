from word import Word
from word import to_ascii
from math import log10


class TargetWord(Word):

    def __init__(self, word, lemma, category_code, text_index, word_index, context, completed_words):
        Word.__init__(self, word, lemma, category_code, text_index, word_index)
        self._context = context
        self._completed_words = map(to_ascii, completed_words)

    def cloze_prob(self, delta):
        "empirical frequency, normalized to avoid probabilities 0 and 1"
        return self._cloze_prob(self.in_ascii(), delta)

    def completed_words(self):
        return self._completed_words

    def was_not_guessed(self):
        return self.in_ascii() not in self.completed_words()

    def everyone_guessed(self):
        return self.completed_words().count(self.in_ascii()) == len(self.completed_words())

    def cloze_entropy(self, delta):
        return -sum([self._cloze_prob(w, delta) * log10(self._cloze_prob(w, delta)) for w in self._completed_words])

    def _cloze_prob(self, word, delta):
        """Calculates the cloze probability from the completed words,
        using delta as smoothing parameter.
        """
        count = float(self._completed_words.count(word))
        total_answers = float(len(self.completed_words()))
        different_answers = float(len(set(self.completed_words())) + 1)
        return (count + delta) / (total_answers + delta * different_answers)

    def context(self):
        return self._context

    def is_target(self):
        return True

    def __repr__(self):
        return "[ %s (%s)]" % (self.in_ascii(), ",".join(self.completed_words()))

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
