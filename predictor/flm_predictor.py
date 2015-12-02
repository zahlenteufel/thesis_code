import sys
import re
import subprocess
from itertools import ifilter
from tempfile import NamedTemporaryFile
from predictor import Predictor


class FLM_Predictor(Predictor):

    def __init__(self, flm_spec):
        Predictor.__init__(self, order=flm_spec.order())
        self.flm_spec = flm_spec

    def batch_predict(self, prediction_text, debug=False):
        """predict all the tagged words in the prediction text,
        i.e. return a list of the probabilities for each word in the lm"""
        return self.logprobs(self.ngrams(prediction_text), debug)

    def normalize(self, word):
        return self.flm_spec.convert_to_flm_format(word)

    def logprobs(self, ngrams, debug=False):
        with NamedTemporaryFile() as f:
            for ngram in ngrams:
                f.write(" ".join(ngram) + "\n")
            f.flush()
            fngram_output = call_fngram(self.flm_spec.factor_file(), f.name)
            if debug:
                print >>sys.stderr, fngram_output
            return parse_fngram_output(fngram_output)

    def name(self):
        return self.flm_spec.factor_file()


def call_fngram(factor_file, text_file):

    # TODO: this only works if it's executed alongside flm_models/ folder.. there must be a better way

    p = subprocess.Popen([
        "fngram",
        "-factor-file", factor_file,
        "-debug", "2",
        "-unk",
        "-no-virtual-begin-sentence",
        "-nonull",
        "-no-virtual-end-sentence",
        "-no-score-sentence-marks",
        "-ppl", text_file],
        stdout=subprocess.PIPE)

    return p.communicate()[0]


def parse_fngram_output(fngram_output):
    lines = iter(ifilter(None, fngram_output.split("\n")))
    line = lines.next()
    sentence_num = 0
    res = []
    while line.startswith("-----"):
        lines.next()
        line = lines.next()
        last_prob = -1000
        while line.startswith("\t"):
            if "[" in line:
                last_prob = float(re.findall(r"\] ([^\s]+) \[", line)[0])
            line = lines.next()
        lines.next()
        lines.next()
        res.append(last_prob)
        line = lines.next()
        sentence_num += 1
    return res
