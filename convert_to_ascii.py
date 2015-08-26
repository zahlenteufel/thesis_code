#!/usr/bin/env python
import io
from predict_this.text.word import to_ascii
from progress_estimator import ProgressEstimator

estimator = ProgressEstimator()

for i in xrange(10000):
    filename = "corpus/tagged_chunks/%s" % str(i).zfill(4)
    if i % 10 == 0:
        print "%.2f %% completed" % (i / 100.0)
        if i:
            print estimator.remaining_time(i / 10000.0)
    with io.open(filename, "r", encoding="utf-8") as corpus:
        with open(filename + ".ascii", "w") as ascii_corpus:
            for line in corpus:
                print >>ascii_corpus, to_ascii(line[:-1])
