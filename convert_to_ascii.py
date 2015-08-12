#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import unidecode

for i in xrange(2500):
    filename = "corpus/resultados/analisis_%s.txt" % str(i).zfill(4)
    with codecs.open(filename, "r", "utf-8") as corpus:
        with codecs.open(filename + ".ascii", "w", "utf-8") as ascii_corpus:
            for line in corpus.readlines():
                print >>ascii_corpus, unidecode.unidecode(line[:-1])
