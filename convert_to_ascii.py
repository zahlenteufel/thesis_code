#!/usr/bin/env python
import codecs
from predict_this.text.word import to_ascii

for i in xrange(10000):
    filename = "corpus/tagged_chunks/%s" % str(i).zfill(4)
    with codecs.open(filename, "r", "utf-8") as corpus:
        with open(filename + ".ascii", "w") as ascii_corpus:
            for line in corpus.readlines():
                print >>ascii_corpus, to_ascii(line[:-1])
