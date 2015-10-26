
class UnigramCachePredictor:

    def batch_predict(self, prediction_texts, debug=False):
        """predict all the tagged words in the prediction text,
        i.e. return a list of the probabilities for each word in the lm"""
        probs = []
        cache = UnigramCache()
        current_prediction_text = -1
        for line in prediction_texts.lines():
            for word in line:
                w = word.in_ascii()
                if word.text_index() != current_prediction_text:
                    current_prediction_text = word.text_index()
                    cache = UnigramCache()
                if word.is_target():
                    probs.append(cache.prob(w))
                cache.add(w)
        return probs

    def batch_entropy(self, prediction_texts):
        return [0] * len(prediction_texts.target_words())

    def name(self):
        return "unigram_cache_predictor"


class UnigramCache:

    def __init__(self):
        self.histogram = {}
        self.total = 0

    def add(self, word):
        self.histogram[word] = self.histogram.get(word, 0) + 1
        self.total += 1

    def prob(self, word):
        return self.histogram.get(word, 1) / float(self.total + 1)
