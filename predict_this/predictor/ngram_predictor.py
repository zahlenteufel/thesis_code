import sys
import re
import subprocess
from more_itertools import peekable
from itertools import izip
from tempfile import NamedTemporaryFile
from predictor import Predictor
from predictor import saturated_last


class NgramPredictor(Predictor):

    def __init__(self, order, ngram_lm=None):
        self.order = order
        self._name = "%d-gram" % order
        self.model_file = ngram_lm or "models/%s.lm.gz" % self._name

    def batch_predict(self, prediction_text, debug=False):
        return self.probs(self.ngrams(prediction_text), debug)

    def target_continuations(self, target, vocabulary):
        context = map(self.normalize, target.context())
        for word in vocabulary:
            return saturated_last(self.order, context + [word])

    def batch_targets_prob_distributions(self, vocabulary, batch_targets):
        batch_queries = (
            query for target in batch_targets
            for query in self.target_continuations(target, vocabulary))
        batch_probs = self.probs(batch_queries)
        for dist in group(batch_probs, len(vocabulary)):
            yield dist

    def print_distribution(self, prediction_text, filename):
        vocabulary = self.vocabulary()
        targets = prediction_text.target_words()
        # To minimize calls to ngram (which has a lot of overhead for loading the model every time),
        # we will group several queries together in batchs.
        number_of_batchs = 200
        batch_size = len(targets) / number_of_batchs
        with open(filename, "w") as file:
            #print header (vocabulary)
            print >>file, " ".join(vocabulary)

            #print body (target - conditional probability distribution for target)
            for batch_targets in group(targets, batch_size):
                batch_dists = self.targets_prob_distributions(vocabulary, batch_targets) 
                for target, dist in izip(batch_targets, batch_dists):
                    print >>file, target, " ".join(dist)

    def vocabulary(self):
        return set(map(lambda l: l.rstrip("\n"), open("corpus/vocabulary.txt")))

    def normalize(self, word):
        return word.in_ascii()

    def probs(self, ngrams, debug=False):
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


def group(list, group_n):
    for i in xrange(0, len(list), group_n):
        yield list[i:(i + group_n)]
