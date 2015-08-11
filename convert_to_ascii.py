#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import unidecode

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

with codecs.open("corpus/tagged_corpus_unic.txt", "r", "utf-8", buffering=4096) as corpus:
    for i, line in enumerate(corpus.readlines()):
        print unidecode.unidecode(line[:-1])
        if i % 10000 == 0:
            sys.stdout.flush()
