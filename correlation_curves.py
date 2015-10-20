import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from predict_this.predictor.ngram_predictor import NgramPredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.predictor.unigram_cache_predictor import UnigramCachePredictor
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.category.category import parse_category_brief, ALL_CATEGORIES, FUNCTION_CATEGORIES, CONTENT_CATEGORIES


def correlation_curve_ngrams(texts, filter_categories, ngram_orders):
    corrs = []
    targets = texts.target_words()
    cloze_probs = HumanPredictor().batch_predict(texts)

    for order in ngram_orders:
        x = []
        y = []

        ngram_probs = NgramPredictor(order).batch_predict(texts)

        for target, cloze_prob, ngram_prob in zip(targets, cloze_probs, ngram_probs):
            if parse_category_brief(target.category_code())["C"] in filter_categories:
                x.append(cloze_prob)
                y.append(ngram_prob)

        lx = logit(x)
        ly = logit(y)

        corrs.append(pearsonr(lx, ly)[0])
    return corrs


def correlation_curve_cache(texts, filter_categories, ngram_order, cache_lambdas):
    corrs = []
    targets = texts.target_words()
    cloze_probs = HumanPredictor().batch_predict(texts)
    ngram_probs = NgramPredictor(ngram_order).batch_predict(texts)

    for cache_lambda in cache_lambdas:
        x = []
        y = []

        cache_probs = UnigramCachePredictor().batch_predict(texts)

        for target, cloze_prob, ngram_prob, cache_prob in zip(targets, cloze_probs, ngram_probs, cache_probs):
            if parse_category_brief(target.category_code())["C"] in filter_categories:
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
    cache_lambdas = map(lambda x: x / 1000.0, xrange(1000))
    function_corrs = correlation_curve_cache(texts, FUNCTION_CATEGORIES, 4, cache_lambdas)
    content_corrs = correlation_curve_cache(texts, CONTENT_CATEGORIES, 4, cache_lambdas) 

    print "max in function corrs", cache_lambdas[function_corrs.index(max(function_corrs))]
    print "max in content corrs", cache_lambdas[content_corrs.index(max(content_corrs))]

    plt.xlabel("cache_lambda")
    plt.ylabel("Correlacion de logit 4-gram y logit cloze variando cache lambda")
    plt.grid(True)
    plt.plot(cache_lambdas, function_corrs, "r-", label="function")
    plt.plot(cache_lambdas, content_corrs, "g:", label="content")
    plt.show()


if __name__ == "__main__":
    text_numbers, orders, categories = parse_arguments()

    texts = PredictionTexts(text_numbers)
    corrs = correlation_curve_ngrams(texts, categories, orders)

    plt.xlabel("orden")
    plt.ylabel("Correlacion de logit n-gram y logit cloze")
    plt.grid(True)
    plt.plot(orders, corrs, "r+-")
    plt.show()

    plot_cache_corr_function_versus_content()
