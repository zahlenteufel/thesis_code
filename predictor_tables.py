from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.predictor.unigram_cache_predictor import UnigramCachePredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.text.word import Word
import sys
from itertools import izip
import argparse

parser = argparse.ArgumentParser(description="Output table with the information of the predictors")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-flm_model_filenames", nargs="*", default=[])
args = parser.parse_args()

prediction_texts = PredictionTexts(args.text_numbers)
predictors = [HumanPredictor(), UnigramCachePredictor()] + \
    [FLM_Specification(flm_model_filename).predictor() for flm_model_filename in args.flm_model_filenames]

# for target_word in prediction_texts.target_words():
    # print map(Word.in_ascii, target_word.context()), target_word
#     print target_word.context()
# predictor = FLM_Specification("flm_models/4gram.flm").predictor()
# for target_word, prediction in izip(prediction_texts.target_words(), predictor.batch_predict(prediction_texts)):
#     print target_word.context(),

# # print header
# print "word", " ".join([predictor.name() for predictor in predictors])

# # print table
all_predictions = zip(*[predictor.batch_predict(prediction_texts) for predictor in predictors])
for target_word, predictions in izip(prediction_texts.target_words(), all_predictions):
    print target_word, " ".join(map(str, predictions))
    sys.stdout.flush()

# ####
# lx = logit(x)
# ly = logit(y)

# xx = np.linspace(min(lx), max(lx), num=100)
# lp = np.poly1d(np.polyfit(lx, ly, 1))

# plt.xlabel("logit cloze_prob")
# plt.ylabel("logit flm pred")

# plt.plot(xx, lp(xx), "r-")
# plt.scatter(lx, ly, alpha=0.2)

# print pearsonr(lx, ly)

# plt.show()
