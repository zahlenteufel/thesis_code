from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_texts import PredictionTexts
from predict_this.predictor.unigram_cache_predictor import UnigramCachePredictor
from predict_this.predictor.human_predictor import HumanPredictor
from predict_this.predictor.ngram_predictor import NgramPredictor
import sys
import io
from itertools import izip
import argparse


def print_predictor_tables(file):
    args = argument_parser()
    prediction_texts = PredictionTexts(args.text_numbers)
    predictors = [HumanPredictor(), UnigramCachePredictor()] + \
        map(NgramPredictor, args.ngram_predictor_orders) + \
        [FLM_Specification(flm_model_filename).predictor() for flm_model_filename in args.flm_model_filenames]
    print_table(file, predictors, prediction_texts, debug=args.debug)


def argument_parser():
    parser = argparse.ArgumentParser(description="Output table with the probabilities given by the predictors")
    parser.add_argument("-text_numbers", type=int, nargs="+", default=[1, 2, 3, 4, 5, 7, 8], help="numbers in [1,2,3,4,5,7,8]")
    parser.add_argument("-ngram_predictor_orders", type=int, nargs="*", default=[])
    parser.add_argument("-flm_model_filenames", nargs="*", default=[])
    parser.add_argument("-debug", type=bool, default=False)
    return parser.parse_args()


def print_table(file, predictors, prediction_texts, debug=False):
    header = ["#texto", "#palabra", "palabra"] + [predictor.name() for predictor in predictors]
    print_row(file, header)

    for target_word, predictions in izip(prediction_texts.target_words(), predictions_table(predictors, prediction_texts, debug)):
        fields = [target_word.text_index(), target_word.word_index(), target_word.original_word()] + predictions
        print_row(file, fields)


def print_row(file, row, separator=u","):
    file.write(separator.join(map(unicode, row)) + u"\n")


def predictions_table(predictors, prediction_texts, debug=False):
    return transpose([predictor.batch_predict(prediction_texts, debug) for predictor in predictors])


def transpose(table):
    return map(list, zip(*table))


if __name__ == "__main__":
    stdout = io.open(sys.stdout.fileno(), "w", encoding="utf-8")
    print_predictor_tables(stdout)
