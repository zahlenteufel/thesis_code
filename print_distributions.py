import argparse
from predict_this.predictor.ngram_predictor import NgramPredictor
from predict_this.text.prediction_text import PredictionText


def argument_parser():
    parser = argparse.ArgumentParser(description="Output the conditional probabilites at the target positions.")
    parser.add_argument("-text_number", type=int, help="number in [1,2,3,4,5,7,8]")
    parser.add_argument("-ngram_predictor_order", type=int)
    parser.add_argument("-ngram_lm", default="")
    parser.add_argument("-output_filename")
    return parser.parse_args()


if __name__ == "__main__":
    args = argument_parser()
    prediction_text = PredictionText(args.text_number)
    ngram_predictor = NgramPredictor(args.ngram_predictor_order, args.ngram_lm)
    ngram_predictor.print_distribution(prediction_text, args.output_filename)
