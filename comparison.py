import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from predict_this.predictor.ngram_predictor import NgramPredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.predictor.unigram_cache_predictor import UnigramCachePredictor
from predict_this.text.prediction_texts import PredictionTexts
import predict_this.category.category as category

parser = argparse.ArgumentParser(description="Plot and calculate correlation between cloze prob and ngram prob.")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-orders", type=int, nargs="+", default=[4], help="order of the n-grams used to calculate ngram prob")
parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(category.ALL_CATEGORIES))
parser.add_argument("-alpha", type=float, default=0.3, help="transparency of the dots in the scatter plot")
parser.add_argument("-cache_lambda", type=float, default=0, help="weight of the unigram cache")
parser.add_argument("-prefix", type=str, default="")
parser.add_argument("-title", type=str)
args = parser.parse_args()

categories = args.categories
if categories == ["all"]:
    categories = category.ALL_CATEGORIES
elif categories == ["function"]:
    categories = category.FUNCTION_CATEGORIES
elif categories == ["content"]:
    categories = category.CONTENT_CATEGORIES

MAX_ORDER = max(args.orders)
predictor = NgramPredictor(MAX_ORDER)


def plot(x, y, lx, ly, order):
    lp = np.poly1d(np.polyfit(lx, ly, 1))
    xx = np.linspace(min(lx), max(lx), num=100)
    if args.title:
        title = args.title
    else:
        title = "Probablity for texts %s\ncategories:%s" % (
            ",".join(map(str, args.text_numbers)),
            ",".join(map(lambda c: category.category_name(c)["category"], categories))
        )
    alpha = args.alpha
    plt.ylabel("logit %d-gram model Probability" % order)
    plt.xlabel("logit Cloze Empirical Probability")
    plt.title(title)
    plt.plot(xx, lp(xx), "r-")
    plt.scatter(lx, ly, alpha=alpha)
    plt.savefig("plots/%slogit_%d.png" % (args.prefix, order))
    plt.close()
    print "correlation %d-gram vs. cloze:" % order, pearsonr(x, y)[0]
    print "correlation %d-gram vs. cloze:" % order, pearsonr(lx, ly)[0]

    p = np.poly1d(np.polyfit(x, y, 1))
    xx = np.linspace(min(x), max(x), num=100)

    plt.ylabel("%d-gram model Probability" % order)
    plt.xlabel("Cloze Empirical Probability")
    plt.title(title)
    plt.plot(xx, p(xx), "r-")
    plt.scatter(x, y, alpha=alpha)
    plt.savefig("plots/%s%d.png" % (args.prefix, order))
    plt.close()


for order in args.orders:
    x = []
    y = []
    prediction_texts = PredictionTexts(args.text_numbers, filter_by=categories)
    targets = prediction_texts.target_words()

    cloze_probs = HumanPredictor().batch_predict(prediction_texts)
    ngram_probs = NgramPredictor(order).batch_predict(prediction_texts)
    cache_probs = UnigramCachePredictor().batch_predict(prediction_texts)

    for target, cloze_prob, ngram_prob, cache_prob in zip(targets, cloze_probs, ngram_probs, cache_probs):
        x.append(cloze_prob)
        y.append(args.cache_lambda * cache_prob + (1 - args.cache_lambda) * ngram_prob)

    lx = logit(x)
    ly = logit(y)
    plot(x, y, lx, ly, order)
