#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import unidecode

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

with codecs.open("corpus/head_tagged_corpus800.txt", "r", "utf-8") as corpus:
    for line in corpus.readlines():
        print unidecode.unidecode(line[:-1])
