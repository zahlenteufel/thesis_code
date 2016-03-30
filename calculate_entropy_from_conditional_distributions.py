import numpy as np
import math
import argparse
from predict_this.text.prediction_text import PredictionText
from predict_this.predictor.unigram_cache_predictor import UnigramCache
from analyze_perplexities import interpolated_with_cache_probability
from itertools import izip


def cache_snapshots(prediction_text):
    cache = UnigramCache()
    for line in prediction_text.lines():
        for word in line:
            w = word.in_ascii()
            if word.is_target():
                yield cache
            cache.add(w)


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
#   [probs[Vngram \ Vcache] interpolados con [0] * N2 +
#   [0] * N1 interpolados con cache[Vcache \ Vngram]]


def combine_cache_probs(cache_lambda, vocab, probs, cache):
    intersection = vocab & cache.vocabulary()
    vocab_only_ngram = list(vocab - intersection)
    vocab_only_cache = list(cache.vocabulary() - intersection)
    intersection = list(intersection)

    def cache_get(w):
        return cache.prob(w, 0.0002)

    i1 = interpolate(cache_lambda, map(cache_get, intersection), map(probs.get, intersection))
    i2 = interpolate(cache_lambda, [0], map(probs.get, vocab_only_ngram))
    i3 = interpolate(cache_lambda, map(cache_get, vocab_only_cache), [0])
    return i1 + i2 + i3


def calculate_entropy_from(filename, cache_text_number=None, cache_lambda=None):
    with open(filename) as file:
        text = PredictionText(cache_text_number)
        vocabulary = file.readline()[:-1].split(" ")
        vocabulary_hash = set(vocabulary)
        for line, cache_snapshot in izip(file, cache_snapshots(text)):
            fields = line[:-1].split(" ")
            target = fields[0]
            probs = map(float, target[1:])
            if cache_text_number is not None:
                probs = combine_cache_probs(
                    cache_lambda,
                    vocabulary_hash,
                    dict(zip(vocabulary, probs)),
                    cache_snapshot)
            best = sorted(zip(probs, vocabulary))[:10]
            print target, entropy(probs), entropy(make_dist([p for p, w in best])), " ".join(best)


def entropy(probs):
    "Calculate normalized entropy"
    n = float(len(probs))
    return -np.math.fsum(map(lambda p: p * math.log10(p), probs)) / math.log10(n)


def make_dist(probs):
    "Rescale the elements to make it a distribution again"
    total = np.math.fsum(probs)
    return [p / total for p in probs]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Calculate entropy from conditional probabilities")
    parser.add_argument("-filename")
    parser.add_argument("-calculate_with_cache", type=bool, action="store_true")
    parser.add_argument("-cache_text_number", type=int, default=None)
    parser.add_argument("-cache_lambda", type=float, default=None)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    if args.calculate_with_cache:
        assert args.cache_text_number is not None
        assert args.cache_lambda is not None
        calculate_entropy_from(args.filename, args.cache_text_number, args.cache_lambda)
    else:
        assert args.cache_text_number is None
        assert args.cache_lambda is None
        calculate_entropy_from(args.filename)
