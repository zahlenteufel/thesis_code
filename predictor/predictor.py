class Predictor:

    def __init__(self, order):
        self.order = order

    def batch_predict(self, prediction_text, debug=False):
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()

    def ngrams(self, prediction_text):
        return [
            map(self.normalize, saturated_last(self.order, target_word.context() + [target_word]))
            for target_word in prediction_text.target_words()
        ]

    def normalize(self, ngram):
        # default: do nothing
        return ngram


def saturated_last(n, l):
    return l[-min(len(l), n):]
