import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
# from scipy.stats.stats import pearsonr
from utils import *
import category
from numpy import log10

parser = argparse.ArgumentParser(description="Plot histograms for ngram_prob, cloze_prob and their correpsonding logit transforms")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-orders", type=int, nargs="+", default=[7], help="order of the n-grams used to calculate ngram prob")
parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(category.ALL_CATEGORIES))
args = parser.parse_args()

categories = args.categories
if categories == ["all"]:
    categories = category.ALL_CATEGORIES
elif categories == ["function"]:
    categories = category.FUNCTION_CATEGORIES
elif categories == ["content"]:
    categories = category.CONTENT_CATEGORIES


predictor = get_predictor_client()

ngram_probs = []
cloze_probs = []
freqs = []

order = 7

for text_number in args.text_numbers:
    for target in get_text_targets(text_number, order)[1]:
        if target.category_code in categories:
            ngram_prob = target.ngram_prob(predictor, order)
            if ngram_prob != 0:
                ngram_probs.append(ngram_prob)
                cloze_probs.append(target.cloze_prob())
                freqs.append(target.frequency)


def plot_hist(title, data, bins=50):
    plt.hist(data, bins)
    # plt.show()
    plt.title("Histograma de %s" % title)
    plt.savefig("%s/histogram_%s.png" % (my_env("PLOTS_PATH"), title))
    plt.close()

plot_hist("ngram_prob", ngram_probs)
plot_hist("logit_ngram_prob", logit(ngram_probs))
plot_hist("cloze_prob", cloze_probs)
plot_hist("logit_cloze_prob", logit(cloze_probs))
plot_hist("CM_freq", freqs)
plot_hist("log10(CM_freq)", log10(freqs))
