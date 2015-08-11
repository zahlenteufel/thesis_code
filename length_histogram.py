from __future__ import division
from collections import defaultdict
from utils import *
from operator import mul
import matplotlib.pyplot as plt


def length_histogram(text):
    profs = defaultdict(lambda: 0)
    for line in text:
        bin = len(line.split(" "))
        profs[bin] += 1
    return zip(*profs.iteritems())


def mean(x, y):
    return sum(map(mul, x, y))


def plot_histogram(text, title, xlim, plot_filename, show=False):
    x, y = length_histogram(text)
    plt.title(title)
    plt.xlabel("Longitud Frase")
    plt.ylabel("Cantidad Frases")
    plt.xlim(xlim)
    plt.plot(x, y)
    m = mean(x, y) / sum(y)
    print "mean:", m
    plt.vlines(m, 0, 1.05 * max(y), color='b', linestyle='dashed', linewidth=2)
    plt.savefig("%s/%s" % (my_env("PLOTS_PATH"), plot_filename))
    if show:
        plt.show()
    plt.close()

CORPUS_PATH = my_env("CORPUS_PATH")
TEXTS_PATH = CORPUS_PATH + "/texts"

plot_histogram(
    open(CORPUS_PATH + "/" + my_env("CORPUS_FILE")).readlines(),
    "Histograma de longitud de frases en el Corpus",
    (2, 70),
    "corpus_depth_histogram.png"
)
texts = sum((open(TEXTS_PATH + "/" + text_info(id)['filename']).read().replace("...", "").split(".") for id in (1, 2, 3, 4, 5, 7, 8)), [])
plot_histogram(
    texts,
    "Histograma de longitud de frases en los textos",
    (2, 100),
    "texts_depth_histogram.png"
)
