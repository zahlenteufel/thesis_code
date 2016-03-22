# -*- coding: utf-8 -*-
from unidecode import unidecode


class Word:

    def __init__(self, word, lemma, category_code, frequency, text_index=-1, word_index=-1):
        self._word = word
        self._lemma = to_ascii(lemma)
        self._category_code = category_code.upper()
        self._text_index = text_index
        self._frequency = int(frequency)
        self._word_index = word_index

    def __str__(self):
        return self.in_ascii()

    def original_word(self):
        return self._word

    def in_ascii(self):
        return to_ascii(self._word)

    def lemma(self):
        return self._lemma

    def category_code(self):
        return self._category_code

    def text_index(self):
        return self._text_index

    def word_index(self):
        return self._word_index

    def frequency(self):
        return self._frequency

    def is_target(self):
        return False


def to_ascii(unicode_word):
    return unidecode(unicode_word.lower().replace(u"ñ", u"ni")).replace("?", "").replace("!", "")
