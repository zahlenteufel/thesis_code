import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from utils import *
from predictor import Predictor
import category

parser = argparse.ArgumentParser(description="Study Correlation.")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-orders", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7], help="order of the n-grams used to calculate ngram prob")
parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(category.ALL_CATEGORIES))
args = parser.parse_args()

categories = args.categories
if categories == ["all"]:
    categories = category.ALL_CATEGORIES
elif categories == ["function"]:
    categories = category.FUNCTION_CATEGORIES
elif categories == ["content"]:
    categories = category.CONTENT_CATEGORIES

info("categories: %s" % categories)

predictor = Predictor(*get_working_model(7))  # get_predictor_client()

corrs = []

for order in args.orders:

    x = []
    y = []

    for text_number in args.text_numbers:
        for target in get_text_targets(text_number, order)[1]:
            if target.category_code.upper() in categories:
                ngram_prob = target.ngram_prob(predictor, order)
                if ngram_prob != 0:
                    x.append(target.cloze_prob())
                    y.append(ngram_prob)

    lx = logit(x)
    ly = logit(y)

    corrs.append(pearsonr(lx, ly)[0])

plt.xlabel("orden")
plt.ylabel("Correlacion de logit n-gram y logit cloze")
plt.plot(args.orders, corrs, "r+-")
plt.show()
