#!/usr/bin/env python
from itertools import izip, count, imap
import numpy as np
import argparse
from math import log
from thesis_code.text.prediction_text import PredictionText
from thesis_code.predictor.unigram_cache_predictor import UnigramCache
from thesis_code.utils.paths import experiments_data_path
from analyze_perplexities import interpolated_with_cache_probability


def group(iterable, n):
    args = [iter(iterable)] * n
    return izip(*args)


def my_open(file, mode="r"):
    return open(experiments_data_path(file), mode)


def get_lines(filename, read_header=False):
    f = my_open(filename)
    if read_header:
        header = f.readline()[:-1].split()
        return header, imap(lambda l: l[:-1], f)
    else:
        return imap(lambda l: l[:-1], f)


def target_probs(text_number):
    header, lines = get_lines("probs_texto_%d.txt" % text_number, True)
    V = int(header.split()[2])
    assert(len(vocab) == V)
    for probs in group(lines, V):
        yield map(float, probs)


def cache_snapshots(prediction_text):
    cache = UnigramCache()
    for line in prediction_text.lines():
        for word in line:
            w = word.in_ascii()
            if word.is_target():
                yield cache
            cache.add(w)


def normalized_entropy(probs):
    V = float(len(probs))
    return -np.math.fsum(p * log(p, 10.0) for p in probs if p) / log(V, 10.0)


def interpolate(cache_lambda, cache_probs, probs):
    if len(cache_probs) == 1:
        cache_probs = [cache_probs[0] / len(probs)] * len(probs)
    elif len(probs) == 1:
        probs = [probs[0] / len(cache_probs)] * len(cache_probs)
    return interpolated_with_cache_probability(cache_lambda, cache_probs, probs)


def combine_cache_probs(cache_lambda, probs, cache):
    vocab = set(probs.keys())
    intersection = vocab & cache.vocabulary()
    vocab_only_ngram = list(vocab - intersection)
    vocab_only_cache = list(cache.vocabulary() - intersection)
    intersection = list(intersection)

    def cache_get(w):
        return cache.prob(w, 0.0)

    i1 = interpolate(cache_lambda, map(cache_get, intersection), map(probs.get, intersection))
    i2 = interpolate(cache_lambda, [0], map(probs.get, vocab_only_ngram))
    i3 = interpolate(cache_lambda, map(cache_get, vocab_only_cache), [0])
    return i1 + i2 + i3


def discard_max_prefix_of_sum_leq(xs, limit):
    total = 0.0
    for i in xrange(len(xs)):
        total += xs[i][0]
        if total > limit:
            break
    return xs[i:]


def create_prunned_dist(probs, vocab, prune_mass=0.99):
    """Prune a distribution so it retains the prune_mass (default 0.99),
    and rescale it so it is a valid distribution again.
    """
    ps = sorted(zip(probs, count(0)))
    ps = discard_max_prefix_of_sum_leq(ps, 1.0 - prune_mass)
    probability_used = np.math.fsum(p for p, _ in ps)
    return dict((vocab[i], p / probability_used) for p, i in ps)


def calculate_entropy_with_cache(cache_lambda, vocab, text_number):
    text = PredictionText(text_number)
    for target, cache, probs in izip(text.target_words(), cache_snapshots(text), target_probs(text_number)):
        dprobs = create_prunned_dist(probs, vocab)
        yield normalized_entropy(combine_cache_probs(cache_lambda, dprobs, cache))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate entropy of n-gram probabilities with cache")
    parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="text numbers")
    parser.add_argument("-cache_lambda", type=float, default=0.22, help="cache lambda")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    vocab = get_lines("corpus_vocabulary.txt")

    for text_number in arguments.text_numbers:
        with my_open("entropy_with_cache_%d" % text_number, "w") as f:
            for entropy in calculate_entropy_with_cache(arguments.cache_lambda, vocab, text_number):
                print >>f, entropy
