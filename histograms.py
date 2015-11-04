import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
# from numpy import log10
import predict_this.category.category as category
from predict_this.predictor.ngram_predictor import NgramPredictor
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.predictor.human_predictor import HumanPredictor


parser = argparse.ArgumentParser(description="Plot histograms for ngram_prob, cloze_prob and their correpsonding logit transforms")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-orders", type=int, nargs="+", default=[4], help="order of the n-grams used to calculate ngram prob")
parser.add_argument("-categories", nargs="*", default=["all"], help="grammatical categories. [%s]" % ", ".join(category.ALL_CATEGORIES))
args = parser.parse_args()

categories = args.categories
if categories == ["all"]:
    categories = category.ALL_CATEGORIES
elif categories == ["function"]:
    categories = category.FUNCTION_CATEGORIES
elif categories == ["content"]:
    categories = category.CONTENT_CATEGORIES


texts = PredictionTexts(args.text_numbers, filter_by=categories)
ngram_predictor = NgramPredictor(max(args.orders))
human_predictor = HumanPredictor()

ngram_probs = ngram_predictor.batch_predict(texts)
cloze_probs = human_predictor.batch_predict(texts)
# freqs = [target.frequency() for target in texts.target_words()]


def plot_hist(title, data, bins=50):
    plt.hist(data, bins)
    # plt.show()
    plt.title("Histograma de %s" % title)
    plt.savefig("plots/histogram_%s.png" % title)
    plt.close()

plot_hist("ngram_prob", ngram_probs)
plot_hist("logit_ngram_prob", logit(ngram_probs))
plot_hist("cloze_prob", cloze_probs)
plot_hist("logit_cloze_prob", logit(cloze_probs))
# plot_hist("CM_freq", freqs)
# plot_hist("log10(CM_freq)", log10(freqs))
