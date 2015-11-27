from itertools import izip, count
import numpy as np
import argparse
from math import log
from predict_this.text.prediction_text import PredictionText
from predict_this.predictor.unigram_cache_predictor import UnigramCache
from analyze_perplexities import interpolated_with_cache_probability


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return izip(*args)


def get_lines(filename):
    return map(lambda l: l[:-1], open(filename))


def target_probs(text_number):
    unk_probs = map(float, get_lines("probs_unk_texto_%d" % text_number))
    with open("probs_texto_%d.txt" % text_number) as f:
        f.readline()  # discard header
        V = int(f.readline()[:-1].split()[2])
        assert(len(vocab) == V)
        for unkprob, probs in izip(unk_probs, grouper(f, V)):
            yield unkprob, map(float, probs)


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
    return -np.math.fsum(map(lambda p: p * log(p, 10.0), probs)) / log(V, 10.0)


def interpolate(cache_lambda, cache_probs, probs):
    if len(cache_probs) == 1:
        cache_probs = [cache_probs[0] / len(probs)] * len(probs)
    elif len(probs) == 1:
        probs = [probs[0] / len(cache_probs)] * len(cache_probs)
    return interpolated_with_cache_probability(cache_lambda, cache_probs, probs)

# hallar cuanto vale unk_prob4, hallar cuantos son los que hay en Vcache \ Vngram. N1
# hallar cuanto vale unk_cache, hallar cuantos hay en Vngram \ Vcache. N2
# el tamano del nuevo vocabulario es .. (usar inclusion-exclusion)
# hallar la entropia de ...
#   [probs[interseccion] interpolados con cache[interseccion] ] +
#   [probs[Vngram \ Vcache] interpolados con [cache[<unk>] / N2] * N2] +
#   [probs[<unk>] / N1] * N1 interpolados con cache[Vcache \ Vngram]]


def combine_cache_probs(cache_lambda, probs, cache):
    vocab = set(probs.keys())
    intersection = vocab & cache.vocabulary()
    vocab_only_ngram = list(vocab - intersection)
    vocab_only_cache = list(cache.vocabulary() - intersection)
    intersection = list(intersection)

    def cache_get(w):
        return cache.prob(w, 0.0002)

    i1 = interpolate(cache_lambda, map(cache_get, intersection), map(probs.get, intersection))
    i2 = interpolate(cache_lambda, map(cache_get, ["<unk>"]), map(probs.get, vocab_only_ngram))
    i3 = interpolate(cache_lambda, map(cache_get, vocab_only_cache), map(probs.get, ["<unk>"]))
    return i1 + i2 + i3


def create_prunned_dist(probs, vocab, prune_N):
    ps = sorted(zip(probs, count(0)))[:prune_N]
    probability_used = np.fsum(p for p, _ in ps)
    # rescale the probabilities
    dprobs = dict((vocab[i], p / probability_used) for p, i in ps)
    dprobs["<unk>"] = 0
    return dprobs


def calculate_entropy_with_cache(cache_lambda, vocab, text_number):
    text = PredictionText(text_number)
    for target, cache, probs4gram in izip(text.target_words(), cache_snapshots(text), target_probs(text_number)):
        unkprob, probs = probs4gram
        dprobs = create_prunned_dist(probs, vocab, 1000)
        yield normalized_entropy(combine_cache_probs(cache_lambda, dprobs, cache))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate entropy of n-gram probabilities with cache")
    parser.add_argument("-text_numbers", type=int, nargs="+", help="text numbers")
    parser.add_argument("-cache_lambda", type=float, default=0.22, help="cache lambda")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    vocab = get_lines("corpus/vocabulary.txt")

    for text_number in arguments.text_numbers:
        with open("entropy_with_cache_%d" % text_number, "w") as f:
            for entropy in calculate_entropy_with_cache(arguments.cache_lambda, vocab, text_number):
                print >>f, entropy
