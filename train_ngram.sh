#!/usr/bin/env bash

[ ! -d models ] && mkdir models

for order in 1 2 3 4; do
	ngram-count -text corpus/corpus_cleaned_normalized.txt -order $order -unk -no-eos -lm models/4-gram.lm.gz;
done
