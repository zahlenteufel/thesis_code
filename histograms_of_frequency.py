import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm
from predict_this.category.category import CONTENT_CATEGORIES
import numpy as np
import pylab

data = []
with open("predict_this/text/texts1234578.csv") as f:
    header = f.next()
    freq_index = header.split(",").index("freq")
    tag_index = header.split(",").index("tag")
    for line in f:
        fields = line.split(",")
        freq = float(fields[freq_index])
        tag = fields[tag_index]
        if tag[0] in CONTENT_CATEGORIES:
            data.append(freq)
            # data.append(math.log10(freq))


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
