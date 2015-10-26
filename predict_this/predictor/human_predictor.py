from ..text.target_word import TargetWord


class HumanPredictor:

    def batch_predict(self, prediction_text, debug=False):
        """predict all the tagged words in the prediction text,
        i.e. return a list of the probabilities for each word in the lm"""
        return map(TargetWord.cloze_prob, prediction_text.target_words())

    def batch_entropy(self, prediction_text):
        return map(TargetWord.cloze_entropy, prediction_text.target_words())

    def name(self):
        return "cloze_predictor"
