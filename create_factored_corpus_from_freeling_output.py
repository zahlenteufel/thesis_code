#!/usr/bin/env python

import os
import predict_this.text.text as Text
import predict_this.flm.flm_specification as FlmSpec
from progress_estimator import ProgressEstimator


FACTORED_CORPUS_FILE = "corpus/factored_corpus_WGNCPL.txt"


def dump_training_file(flm_spec, output_file):
    progress_estimator = ProgressEstimator()
    for i in xrange(10000):
        index = str(i).zfill(4)
        tagged_filename = "corpus/tagged_chunks/%s.ascii" % index
        tagged_text = Text.Text.from_freeling_output_file(tagged_filename)
        # TODO: use tmpfiles
        factored_chunks_folder = "corpus/factored_chunks"
        ensure_folder(factored_chunks_folder)
        with open(factored_chunks_folder + "/" + index, "w") as factored_file:
            for tagged_line in tagged_text.lines():
                factored_file.write(" ".join(map(flm_spec.convert_to_flm_format, tagged_line)) + "\n")
        if i and i % 10 == 0:
            print "\rfactoring... %.2f%%" % (100 * i / 10000.0), progress_estimator.remaining_time(i / 10000.0),
    # print "done factoring chunks, concatenating"
    # os.system("./concatenate_files.sh corpus/factored_chunks/ \"*\" " + output_file)


def ensure_folder(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

if not os.path.isfile(FACTORED_CORPUS_FILE):
    flm_spec = FlmSpec.FLM_Specification("flm_models/WGNCPL.flm.dummy")
    dump_training_file(flm_spec, "corpus/factored_corpus_WGNCPL.txt")
