from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_text import PredictionText
from itertools import izip
import sys

assert len(sys.argv) == 3, "Invalid Parameters"

text_number = int(sys.argv[1])
flm_model_filename = sys.argv[2]

prediction_text = PredictionText(text_number)
predictor = FLM_Specification(flm_model_filename).predictor()

longest_length = max(map(lambda t: len(t.actual_word().in_ascii()), prediction_text.target_words()))

for target_word, prediction in izip(prediction_text.target_words(), predictor.batch_predict(prediction_text)):
    print "%s%f   %f" % (
        target_word.actual_word().in_ascii().ljust(longest_length + 1),
        target_word.cloze_prob(),
        prediction)
