from itertools import izip
import numpy as np
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
    with open("logprobs_texto_%d.txt" % text_number) as f:
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


def interpolate(a, b, cache_lambda):
    if len(a) == 1:
        a = [a[0] / len(b)] * len(b)
    elif len(b) == 1:
        b = [b[0] / len(a)] * len(a)
    return interpolated_with_cache_probability(cache_lambda, a, b)

# hallar cuanto vale unk_prob4, hallar cuantos son los que hay en Vcache \ Vngram. N1
# hallar cuanto vale unk_cache, hallar cuantos hay en Vngram \ Vcache. N2
# el tamano del nuevo vocabulario es .. (usar inclusion-exclusion)
# hallar la entropia de ...
#   [probs[interseccion] interpolados con cache[interseccion] ] +
#   [probs[Vngram \ Vcache] interpolados con [cache[<unk>] / N2] * N2] +
#   [probs[<unk>] / N1] * N1 interpolados con cache[Vcache \ Vngram]]


def combine_cache_probs(cache_lambda, vocab, probs, cache):
    intersection = vocab & cache.vocabulary()
    vocab1 = list(vocab - intersection)
    vocab2 = list(cache.vocabulary() - intersection)
    intersection = list(intersection)

    def cache_get(w):
        return cache.prob(w, 0.0002)

    return \
        interpolate(map(probs.get, intersection), map(cache_get, intersection), cache_lambda) + \
        interpolate(map(probs.get, vocab1), map(cache_get, ["<unk>"]), cache_lambda) + \
        interpolate(map(probs.get, ["<unk>"]), map(cache_get, vocab2), cache_lambda)


def calculate_entropy_with_cache(cache_lambda, vocab, text_number):
    text = PredictionText(text_number)
    vocab_hash = set(vocab)
    for target, cache, probs4gram in izip(text.target_words(), cache_snapshots(text), target_probs(text_number)):
        unkprob, probs = probs4gram
        dprobs = dict(zip(vocab, probs4gram))
        dprobs["<unk>"] = unkprob
        yield normalized_entropy(combine_cache_probs(cache_lambda, vocab_hash, dprobs, cache))


print "cargando vocabulario.. ",
vocab = set(map(lambda l: l[:-1], open("corpus/vocabulary.txt")))
print "listo"

for text_number in (1, 2, 3, 4, 5, 7, 8):
    for entropy in calculate_entropy_with_cache(0.22, vocab, text_number):
        print entropy
