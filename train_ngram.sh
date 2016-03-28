#!/usr/bin/env bash

[ ! -d models ] && mkdir models

ngram-count -text corpus/corpus_cleaned_normalized.txt -order 4 -unk -no-eos -lm models/4-gram.lm.gz

# The 4-gram model includes the {1,2,3}-gram models.

ln -s models/4-gram.lm.gz models/3-gram.lm.gz
ln -s models/4-gram.lm.gz models/2-gram.lm.gz
ln -s models/4-gram.lm.gz models/1-gram.lm.gz
