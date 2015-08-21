from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.predictor.unigram_cache_predictor import UnigramCachePredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.predictor.ngram_predictor import NgramPredictor
import sys
from itertools import izip
import argparse

parser = argparse.ArgumentParser(description="Output table with the information of the predictors")
parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
parser.add_argument("-ngram_predictor_orders", type=int, nargs="*", default=[])
parser.add_argument("-flm_model_filenames", nargs="*", default=[])
parser.add_argument("-debug", type=bool, default=False)
args = parser.parse_args()

prediction_texts = PredictionTexts(args.text_numbers)
predictors = [HumanPredictor(), UnigramCachePredictor()] + \
    map(NgramPredictor, args.ngram_predictor_orders) + \
    [FLM_Specification(flm_model_filename).predictor() for flm_model_filename in args.flm_model_filenames]

# print header
print "word", " ".join([predictor.name() for predictor in predictors])

# print table
all_predictions = zip(*[predictor.batch_predict(prediction_texts, args.debug) for predictor in predictors])
for target_word, predictions in izip(prediction_texts.target_words(), all_predictions):
    print target_word, " ".join(map(lambda prediction: "%f,%f" % prediction, predictions))
    sys.stdout.flush()
