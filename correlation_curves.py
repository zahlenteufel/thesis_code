import matplotlib.pyplot as plt
import argparse
from scipy.special import logit
from scipy.stats.stats import pearsonr
from predict_this.predictor.ngram_predictor import NgramPredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.category.category import parse_category_brief, ALL_CATEGORIES, FUNCTION_CATEGORIES, CONTENT_CATEGORIES

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

corrs = []

texts = PredictionTexts(args.text_numbers)
targets = texts.target_words()
cloze_probs = HumanPredictor().batch_predict(texts)

for order in args.orders:
    x = []
    y = []

    ngram_probs = NgramPredictor(order).batch_predict(texts)

    for target, cloze_prob, ngram_prob in zip(targets, cloze_probs, ngram_probs):
        if parse_category_brief(target.category_code())["C"] in categories:
            assert cloze_prob != 0 and cloze_prob != 1
            x.append(cloze_prob)
            y.append(ngram_prob)

    lx = logit(x)
    ly = logit(y)

    corrs.append(pearsonr(lx, ly)[0])

print args.orders, corrs

plt.xlabel("orden")
plt.ylabel("Correlacion de logit n-gram y logit cloze")
plt.grid(True)
plt.plot(args.orders, corrs, "r+-")
plt.show()
