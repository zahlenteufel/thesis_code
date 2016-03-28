import io
import sys
sys.path.insert(0, "..")  # for using predict_this module
from predict_this.text.word import to_ascii

with io.open("corpus_cleaned.txt", "r", encoding="utf-8") as corpus:
    with open("corpus_cleaned_normalized.txt", "w") as ascii_corpus:
        for line in corpus:
            print >>ascii_corpus, to_ascii(line[:-1])
