#!/usr/bin/env python
import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from thesis_code.predictor.ngram_predictor import NgramPredictor
from thesis_code.predictor.human_predictor import HumanPredictor
from thesis_code.predictor.unigram_cache_predictor import UnigramCachePredictor
from thesis_code.text.prediction_texts import PredictionTexts
from thesis_code.category.category import ALL_CATEGORIES, FUNCTION_CATEGORIES, CONTENT_CATEGORIES


def correlation_curve_ngrams(texts, ngram_orders):
    corrs = []
    targets = texts.target_words()
    cloze_probs = HumanPredictor().batch_predict(texts)

    for order in ngram_orders:
        x = []
        y = []

        ngram_probs = NgramPredictor("../corpus/4gram.lm.gz", order).batch_predict(texts)

        for target, cloze_prob, ngram_prob in zip(targets, cloze_probs, ngram_probs):
            x.append(cloze_prob)
            y.append(ngram_prob)

        lx = logit(x)
        ly = logit(y)

        corrs.append(pearsonr(lx, ly)[0])
    return corrs


def correlation_curve_cache(texts, ngram_order, cache_lambdas):
    corrs = []
    targets = texts.target_words()
    cloze_probs = HumanPredictor().batch_predict(texts)
    ngram_probs = NgramPredictor("../corpus/4gram.lm.gz", ngram_order).batch_predict(texts)

    for cache_lambda in cache_lambdas:
        x = []
        y = []

        cache_probs = UnigramCachePredictor().batch_predict(texts)

        for target, cloze_prob, ngram_prob, cache_prob in zip(targets, cloze_probs, ngram_probs, cache_probs):
            x.append(cloze_prob)
            y.append(cache_lambda * cache_prob + (1 - cache_lambda) * ngram_prob)

        lx = logit(x)
        ly = logit(y)

        corrs.append(pearsonr(lx, ly)[0])
    return corrs


def parse_arguments():
    parser = argparse.ArgumentParser(description="Study Correlation.")
    parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
    parser.add_argument("-orders", type=int, nargs="+", default=[1, 2, 3, 4], help="order of the n-grams used to calculate ngram prob")
    parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(ALL_CATEGORIES))
    args = parser.parse_args()

    categories = args.categories
    if categories == ["all"]:
        categories = ALL_CATEGORIES
    elif categories == ["function"]:
        categories = FUNCTION_CATEGORIES
    elif categories == ["content"]:
        categories = CONTENT_CATEGORIES

    return args.text_numbers, args.orders, categories


def plot_cache_corr_function_versus_content():
    texts_content = PredictionTexts(text_numbers, filter_by=CONTENT_CATEGORIES)
    texts_function = PredictionTexts(text_numbers, filter_by=FUNCTION_CATEGORIES)
    N = 100
    cache_lambdas = map(lambda x: x / float(N), xrange(N))
    function_corrs = correlation_curve_cache(texts_function, 4, cache_lambdas)
    content_corrs = correlation_curve_cache(texts_content, 4, cache_lambdas)

    print "max in function corrs", cache_lambdas[function_corrs.index(max(function_corrs))]
    print "max in content corrs", cache_lambdas[content_corrs.index(max(content_corrs))]

    plt.xlabel("$\lambda_{cache}$")
    plt.ylabel("Correlacion de logit 4-gram y logit cloze")
    plt.grid(True)
    plt.plot(cache_lambdas, function_corrs, "r--")
    plt.plot(cache_lambdas, content_corrs, "g-")
    plt.legend(["funcion", "contenido"])
    plt.show()


if __name__ == "__main__":
    text_numbers, orders, categories = parse_arguments()

    texts = PredictionTexts(text_numbers, filter_by=categories)
    corrs = correlation_curve_ngrams(texts, orders)

    plt.xlabel("orden")
    plt.ylabel("Correlacion de logit n-gram y logit cloze")
    plt.grid(True)
    plt.plot(orders, corrs, "r+-")
    plt.show()

    # plot_cache_corr_function_versus_content()
