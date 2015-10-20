import io
from predict_this.text.word import to_ascii

with io.open("corpus/corpus_cleaned.txt", "r", encoding="utf-8") as corpus:
    with open("corpus/corpus_cleaned_normalized.txt", "w") as ascii_corpus:
        for line in corpus:
            print >>ascii_corpus, to_ascii(line[:-1])
