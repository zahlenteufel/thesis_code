import matplotlib.pyplot as plt
import numpy as np
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from utils import *
# from predictor import Predictor, get_text_targets
import category

parser = argparse.ArgumentParser(description="Plot and calculate correlation between cloze prob and ngram prob.")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-orders", type=int, nargs="+", default=[7], help="order of the n-grams used to calculate ngram prob")
parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(category.ALL_CATEGORIES))
parser.add_argument("-alpha", type=float, default=0.3, help="transparency of the dots in the scatter plot")
parser.add_argument("-cache_lambda", type=float, default=0, help="weight of the unigram cache")
parser.add_argument("-prefix", type=str, default="")
parser.add_argument("-title", type=str)
parser.add_argument('-dump', dest='dump', type=str, help="flag to just output the points instead of plotting")
args = parser.parse_args()

categories = args.categories
if categories == ["all"]:
    categories = category.ALL_CATEGORIES
elif categories == ["function"]:
    categories = category.FUNCTION_CATEGORIES
elif categories == ["content"]:
    categories = category.CONTENT_CATEGORIES

info("categories: %s" % categories)

# MAX_ORDER = max(args.orders)
# predictor = Predictor(*get_working_model(MAX_ORDER))
predictor = get_predictor_client()


def plot(x, y, lx, ly):
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
    plt.savefig("%s/%slogit_%d.png" % (my_env("PLOTS_PATH"), args.prefix, order))
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
    plt.savefig("%s/%s%d.png" % (my_env("PLOTS_PATH"), args.prefix, order))
    plt.close()

for order in args.orders:

    x = []
    y = []
    extra_info = []

    for text_number in args.text_numbers:
        _, targets = get_text_targets(text_number, order)
        for target in targets:
            if target.category_code.upper() in categories:
                ngram_prob = target.ngram_prob(predictor, 7, args.cache_lambda)
                if ngram_prob != 0:
                    x.append(target.cloze_prob())
                    y.append(ngram_prob)
                    extra_info.append((target.text_number, target.target_index))

    lx = logit(x)
    ly = logit(y)

    if args.dump:
        for px, py, (text_number, target_index) in izip(lx, ly, target):
            print args.dump.replace("LX", str(px)).replace("LY", str(py)).replace("FN", str(text_number)).replace("I", str(target_index))
    else:
        plot(x, y, lx, ly)
