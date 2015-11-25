from collections import deque


class UnigramCachePredictor:

    def __init__(self, delta=0.0002, limit=None):
        self.delta = delta
        self.limit = limit

    def batch_predict(self, prediction_texts, debug=False):
        """predict all the tagged words in the prediction text,
        i.e. return a list of the probabilities for each word in the lm"""
        probs = []
        cache = UnigramCache(self.limit)
        current_prediction_text = -1
        for line in prediction_texts.lines():
            for word in line:
                w = word.in_ascii()
                if word.text_index() != current_prediction_text:
                    current_prediction_text = word.text_index()
                    cache = UnigramCache(self.limit)
                if word.is_target():
                    probs.append(cache.prob(w, self.delta))
                cache.add(w)
        return probs

    def batch_entropy(self, prediction_texts, save_probs=False):
        # dummy values..
        return [0] * len(prediction_texts.target_words())

    def name(self):
        return "unigram_cache_predictor"


class UnigramCache:

    def __init__(self, limit=None):
        self.histogram = {}
        self.total = 0
        self.limit = limit
        self.history = deque()

    def add(self, word):
        self.histogram[word] = self.histogram.get(word, 0) + 1
        self.total += 1
        if self.limit and self.total > self.limit:
            self._remove_last()
        self.history.append(word)

    def _remove_last(self):
        last = self.history.popleft()
        self.histogram[last] -= 1
        if self.histogram[last] == 0:
            del self.histogram[last]
        self.total -= 1

    def prob(self, word, delta):
        count = float(self.histogram.get(word, 0))
        total = float(self.total)
        vocabulary = float(len(self.histogram) + 1)  # + 1 for the <unk>
        return (count + delta) / (total + delta * vocabulary)

    def vocabulary(self):
        return set(self.histogram.keys())
