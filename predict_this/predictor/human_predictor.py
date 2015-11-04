
class HumanPredictor:

    def __init__(self, delta=0.28):
        self.delta = delta

    def batch_predict(self, prediction_text, debug=False):
        """predict all the tagged words in the prediction text,
        i.e. return a list of the probabilities for each word in the lm"""
        return [target.cloze_prob(self.delta) for target in prediction_text.target_words()]

    def batch_entropy(self, prediction_text, delta):
        return [target.cloze_entropy(delta) for target in prediction_text.target_words()]

    def name(self):
        return "cloze_predictor"
