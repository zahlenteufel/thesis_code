#!/usr/bin/env python
from thesis_code.text.prediction_texts import PredictionTexts
from thesis_code.predictor.unigram_cache_predictor import UnigramCachePredictor
from thesis_code.predictor.ngram_predictor import NgramPredictor
from analyze_perplexities import interpolated_with_cache_probability, predictor_perplexity
import matplotlib.pyplot as plt


def cache_different_limits(limits):
    prediction_texts = PredictionTexts([1, 2, 3, 4, 5, 7, 8])
    ngram_predictions = NgramPredictor(None, order=4).batch_predict(prediction_texts)
    perplexities = []
    for limit in limits:
        perplexity = predictor_perplexity(
            interpolated_with_cache_probability(
                0.22,
                UnigramCachePredictor(limit=limit).batch_predict(prediction_texts),
                ngram_predictions
            )
        )
        perplexities.append(perplexity)
        print limit, perplexity
    plt.ylabel("Perplexity")
    plt.xlabel("Limite de Cache")
    plt.plot(limits, perplexities, ".-")
    plt.show()


if __name__ == "__main__":
    limits = (10, 100, 200, 400, 800, 1600, 3200, 6000)
    cache_different_limits(limits)
