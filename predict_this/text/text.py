import codecs
from ..category.analyze_syntax import analyze, analyze_freeling_output
from word import Word


class Text:

    @classmethod
    def from_flat_file(self, filename):
        with codecs.open(filename, "r", "utf-8") as file:
            tagged_lines = analyze(file.read())
            return Text.from_tagged_lines(tagged_lines)

    @classmethod
    def from_freeling_output_file(self, filename):
        with codecs.open(filename, "r", "utf-8") as file:
            tagged_lines = analyze_freeling_output(file.read())
            return Text.from_tagged_lines(tagged_lines)

    @classmethod
    def from_tagged_lines(self, tagged_lines):
        lines = [
            [Word(word, category_code) for word, _, category_code in tagged_line]
            for tagged_line in tagged_lines
        ]
        return Text()._initialize_with_lines(lines)

    def _initialize_with_lines(self, lines):
        self._lines = lines
        return self

    def lines(self):
        return self._lines

    def __str__(self):
        return u"\n".join([u" ".join(map(unicode, line)) for line in self._lines])
