from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_text import PredictionText
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import logit
from scipy.stats.stats import pearsonr
from itertools import izip
import sys

assert len(sys.argv) == 3, "Invalid Parameters"

text_number = int(sys.argv[1])
flm_model_filename = sys.argv[2]

prediction_text = PredictionText(text_number)
predictor = FLM_Specification(flm_model_filename).predictor()

longest_length = max(map(lambda t: len(t.actual_word().in_ascii()), prediction_text.target_words()))

x = []
y = []
for target_word, prediction in izip(prediction_text.target_words(), predictor.batch_predict(prediction_text)):
    print "%s%f   %f" % (
        target_word.actual_word().in_ascii().ljust(longest_length + 1),
        target_word.cloze_prob(),
        prediction)
    if prediction != -1:
        x.append(target_word.cloze_prob())
        y.append(prediction)

####
lx = logit(x)
ly = logit(y)

xx = np.linspace(min(lx), max(lx), num=100)
lp = np.poly1d(np.polyfit(lx, ly, 1))

plt.xlabel("logit cloze_prob")
plt.ylabel("logit flm pred")

plt.plot(xx, lp(xx), "r-")
plt.scatter(lx, ly, alpha=0.2)

print pearsonr(lx, ly)

plt.show()
