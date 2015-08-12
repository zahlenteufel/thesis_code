from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_text import PredictionText
from itertools import izip

prediction_text = PredictionText(1)
predictor = FLM_Specification("flm_models/bigramWG.flm").predictor()

for target_word, prediction in izip(prediction_text.target_words(), predictor.batch_predict(prediction_text)):
    print target_word.actual_word, target_word.cloze_prob(), prediction
