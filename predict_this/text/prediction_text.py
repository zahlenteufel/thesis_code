import csv
from itertools import ifilter
from target_word import TargetWord
from word import Word
import os

from ..category.category import parse_category_brief


class PredictionText:
    """
    This class loads the experiments texts: that is text with
    'holes' (TargetWords) on it that people have to guess.
    """

    def __init__(self, text_index, filter_by=None):
        self.filter_by = filter_by
        assert(text_index in [1, 2, 3, 4, 5, 7, 8])
        with open(os.path.dirname(os.path.realpath(__file__)) + "/texts1234578.csv", "r") as csvfile:
            reader = UnicodeDictReader(csvfile, delimiter=',')
            text_builder = TextBuilder(text_index, reader)
            self._lines = list(text_builder.lines())

    def lines(self):
        return self._lines

    def target_words(self):
        return [
            word for line in self.lines() for word in line
            if word.is_target() and
            (self.filter_by is None or parse_category_brief(word.category_code())["C"] in self.filter_by)
        ]


class TextBuilder:

    def __init__(self, text_index, reader):
        self.reader = ifilter(lambda row: int(row["text_index"]) == text_index, reader)
        self.text_index = text_index
        self.word_index = 0

    def lines(self):
        current_line = self.new_line()
        current_sentece_num = 1
        for row in self.reader:
            self.word_index += 1
            row["word_index"] = self.word_index
            row["sentence_number"] = int(row["sentence_number"])
            if row["sentence_number"] != current_sentece_num:
                yield current_line
                current_line = self.new_line()
                current_sentece_num = row["sentence_number"]
            word = TargetWord.from_csv_row(row, current_line)
            current_line.append(word)
        if current_line:
            yield current_line

    def new_line(self):
        return [Word(
            word="<s>",
            lemma="NULL",
            category_code="",
            text_index=self.text_index,
            word_index=-1,
        )]


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}
