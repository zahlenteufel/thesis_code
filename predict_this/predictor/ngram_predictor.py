import sys
import re
import subprocess
from more_itertools import peekable
from tempfile import NamedTemporaryFile
from predictor import Predictor
from predictor import saturated_last
import numpy as np


class NgramPredictor(Predictor):

    def __init__(self, ngram_lm, order):
        self.order = order
        self._name = "%dgram" % order
        self.model_file = ngram_lm or "corpus/%s.lm.gz" % self._name

    def batch_predict(self, prediction_text, debug=False):
        return self.logprobs(self.ngrams(prediction_text), debug)

    def batch_entropy(self, prediction_text, save_logprobs=False):
        vocabulary = self.vocabulary()
        targets = prediction_text.target_words()
        number_of_chunks = 200
        chunk_size = len(targets) / number_of_chunks
        result = []
        if save_logprobs:
            f_logprobs = open("logprobs.txt")
            print >>f_logprobs, "# list of logprobs for %d-gram (%s)" % (self.order, self.model_file)
            print >>f_logprobs, "# vocabulary-size: %d" % len(vocabulary)
        for i in xrange(0, len(targets), chunk_size):
            chunk_targets = targets[i:min(len(targets), i + chunk_size)]
            with NamedTemporaryFile() as f:
                for j, target in enumerate(chunk_targets):
                    context = map(self.normalize, target.context())
                    for word in vocabulary:
                        print >>f, " ".join(saturated_last(self.order, context + [word]))
                f.flush()

                p = subprocess.Popen([
                    "ngram",
                    "-order", str(self.order),
                    "-lm", self.model_file,
                    "-debug", "2",
                    "-unk",
                    "-no-eos",
                    "-no-sos",
                    "-ppl", f.name],
                    stdout=subprocess.PIPE)
                ngram_output = p.communicate()[0]
                logprobs = parse_ngram_output(len(chunk_targets) * len(vocabulary), ngram_output)
                for i in xrange(0, len(logprobs), len(vocabulary)):
                    ent = calculate_entropy(logprobs[i:(i + len(vocabulary))])
                    if save_logprobs:
                        for logprob in logprobs[i:(i + len(vocabulary))]:
                            print >>f_logprobs, logprob
                    result.append(ent)
        if save_logprobs:
            f_logprobs.close()
        return result

    def vocabulary(self):
        return set(map(lambda l: l.rstrip("\n"), open("corpus/vocabulary.txt")))

    def normalize(self, word):
        return word.in_ascii()

    def logprobs(self, ngrams, debug=False):
        with NamedTemporaryFile() as f:
            for ngram in ngrams:
                f.write(" ".join(ngram) + "\n")
            f.flush()
            ngram_output = self.call_ngram(f.name)
            if debug:
                print >>sys.stderr, ngram_output
            return parse_ngram_output(len(ngrams), ngram_output)

    def name(self):
        return self._name

    def call_ngram(self, text_filename):
        p = subprocess.Popen([
            "ngram",
            "-order", str(self.order),
            "-lm", self.model_file,
            "-debug", "2",
            "-unk",
            "-no-eos",
            "-no-sos",
            "-ppl", text_filename],
            stdout=subprocess.PIPE)
        return p.communicate()[0]


def parse_ngram_output(ngrams_len, ngram_output):
    lines = peekable(ngram_output.split("\n"))
    res = []
    for i in xrange(ngrams_len):
        line = lines.next()
        while lines.peek().startswith("\t"):
            line = lines.next()
        m = re.findall(r"\] ([^\s]+) \[", line)
        if m:
            last_prob = float(m[0])
        else:
            print >>sys.stderr, "ERROR parsing lastprob: %s" % line
        lines.next()
        lines.next()
        res.append(last_prob)
        lines.next()
    return res


def calculate_entropy(logprobs):
    return -np.math.fsum(map(lambda lp: lp * pow(10.0, lp), logprobs))
