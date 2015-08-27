#!/usr/bin/env python

from datetime import datetime
import os
import glob
import predict_this.text.text as Text
import predict_this.flm.flm_specification as FlmSpec

LOG_FILENAME = "training.log"

log_file = open(LOG_FILENAME, "a")


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def log(s):
    s = now() + ": " + s
    print s
    print >>log_file, s
    log_file.flush()


FACTORED_CORPUS_FILE = "corpus/factored_corpus_WGNCPL.txt"


def dump_training_file(flm_spec, output_file):
    for i in xrange(10000):
        index = str(i).zfill(4)
        tagged_filename = "corpus/tagged_chunks/%s.ascii" % index
        tagged_text = Text.Text.from_freeling_output_file(tagged_filename)
        # TODO: use tmpfiles
        with open("corpus/factored_chunks/" + index, "w") as factored_file:
            for tagged_line in tagged_text.lines():
                factored_file.write(" ".join(map(flm_spec.convert_to_flm_format, tagged_line)) + "\n")
        if i % 100 == 0:
            log("factoring... %d%%" % i / 100)
    log("done factoring chunks, concatenating")
    os.system("./concatenate_files.sh corpus/factored_chunks/ \"*\" " + output_file)


if not os.path.isfile(FACTORED_CORPUS_FILE):
    flm_spec = FlmSpec.FLM_Specification("flm_models/WGNCP.flm.dummy")
    dump_training_file(flm_spec, "corpus/factored_corpus_WGNCP.txt")
    # TODO: execute this directly..
    assert False, "now you have to execute factors_zip_lemmas.py in corpus"

with open("train_all_models.sh", "w") as training_script:
    print >>training_script, "#!/usr/bin/env bash\n"
    print >>training_script, "# AUTOGENERATED SCRIPT at %s \n" % now()

    any_training_necessary = False

    for flm_model_filename in glob.glob("flm_models/*.flm"):

        flm_spec = FlmSpec.FLM_Specification(flm_model_filename)

        if os.path.isfile(flm_spec.model_file()):
            log("'%s' already exists, skip training." % flm_spec.model_file())
        else:
            any_training_necessary = True
            assert flm_spec.factors() <= {"W", "G", "N", "C", "P", "L"}, " must use common factors only.. (%s)" % flm_spec.model_file()
            print >>training_script, "echo \"$(date): training %s\" | tee -a %s" % (flm_model_filename, LOG_FILENAME)
            print >>training_script, "fngram-count -factor-file %s -no-virtual-end-sentence -unk -lm -write-counts -text %s" % \
                (flm_model_filename, FACTORED_CORPUS_FILE)

    if any_training_necessary:
        print >>training_script, "echo \"$(date): finished training\" | tee -a ", LOG_FILENAME
        log("done factoring and creating script for training")
        print
        print "Factored files, prepared script for training."
        print "To continue training execute ./train_all_models.sh"
    else:
        log("there is nothing to be trained")
