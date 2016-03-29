import sys
import re
import subprocess
from more_itertools import peekable
from itertools import izip, islice
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

    def print_distribution(self, prediction_text, filename):
        vocabulary = self.vocabulary()
        targets = prediction_text.target_words()
        with open(filename, "w") as file:
            # print header (vocabulary)
            print >>file, " ".join(vocabulary)

            queries = (
                query for target in targets
                for query in self.target_continuations(target, vocabulary))
            distributions = group(self.probs(queries, batch_size=40), len(vocabulary))
            for target, distribution in izip(targets, distributions):
                print >>file, target, " ".join(distribution)

    def vocabulary(self):
        return set(map(lambda l: l.rstrip("\n"), open("corpus/vocabulary.txt")))

    def normalize(self, word):
        return word.in_ascii()

    def probs(self, queries, debug=False, batch_size=None):
        for queries_batch in group(queries, batch_size):
            with NamedTemporaryFile() as f:
                for query in queries:
                    f.write(" ".join(query) + "\n")
                f.flush()
                ngram_output = self.call_ngram(f.name)
                if debug:
                    print >>sys.stderr, ngram_output
                for prob in parse_ngram_output(len(queries_batch), ngram_output):
                    yield prob

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


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


def group(l, group_n):
    if group_n is None:
        yield l
    else:
        while True:
            res = take(group_n, l)
            if not res:
                break
            yield res
