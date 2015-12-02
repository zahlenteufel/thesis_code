#!/usr/bin/env python
from thesis_code.text.prediction_text import PredictionText
from thesis_code.predictor.ngram_predictor import NgramPredictor


def adhoc_preds(predictor, text):
    UNK = "fjwnjw22883"
    queries = [ngram[:-1] + [UNK] for ngram in predictor.ngrams(text)]
    return predictor.probs(queries)

predictor = NgramPredictor(None, 4)
for text_number in (1, 2, 3, 4, 5, 7, 8):
    with open("probs_unk_texto_%d" % text_number, "w") as f:
        text = PredictionText(text_number)
        for prob in adhoc_preds(predictor, text):
            print >>f, prob
