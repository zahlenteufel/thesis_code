import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm
from predict_this.category.category import CONTENT_CATEGORIES
from predict_this.text.prediction_texts import PredictionTexts
import numpy as np
import pylab

words = PredictionTexts([1, 2, 3, 4, 5, 7, 8]).words()
data = [word.frequency() for word in PredictionTexts([1, 2, 3, 4, 5, 7, 8]).words(filter_by=CONTENT_CATEGORIES)]

y, binEdges = np.histogram(data, bins=80)
bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
pylab.plot(bincenters, y, '-')
pylab.ylabel("Cantidad de Palabras")
pylab.xlabel("Frecuencia")
pylab.xlim((0, 12000))
pylab.show()

y, binEdges = np.histogram(np.log10(data), bins=100, normed=True)
bincenters = 0.5 * (binEdges[1:] + binEdges[:-1])
pylab.plot(bincenters, y, '-')
pylab.ylabel("Cantidad de Palabras")
pylab.xlabel("log10(Frecuencia)")


(mu, sigma) = norm.fit(np.log10(data))
y = mlab.normpdf(bincenters, mu, sigma)
l = plt.plot(bincenters, y, 'r--', linewidth=2)
pylab.show()
