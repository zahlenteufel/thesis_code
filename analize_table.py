import matplotlib.pyplot as plt
from itertools import izip
from scipy.special import logit
from scipy.stats.stats import pearsonr
import math
import sys

# USAGE:
# pipe the results of predictor_tables


def select(table, column):
    return [row[column] for row in table]


def filter_valid(x1, x2):
    return zip(*[
        (e1, e2) for e1, e2 in izip(x1, x2) if
        not math.isinf(e1) and
        not math.isinf(e2) and
        not math.isnan(e1) and
        not math.isnan(e2)])

header = sys.stdin.readline()[:-1].split()[1:]
table_probs = []
table_ppls = []
while True:
    row = sys.stdin.readline()[:-1].split()
    if not row:
        break
    word, nums = row[0], map(lambda p: tuple(map(float, p.split(","))), row[1:])

    probs, ppls = zip(*nums)
    if any(map(lambda x: x == 0, probs)):
        print word, probs

    table_probs.append(probs)
    table_ppls.append(ppls)


def plot(x, y, xlabel, ylabel, title):
    plt.close()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(x, y, alpha=0.2)
    plt.title(title)
    print pearsonr(x, y)[0]
    plt.show()


def logit_plot(x, y, xlabel, ylabel, title):
    plot(logit(x), logit(y), "logit " + xlabel, "logit " + ylabel, title)


n = len(header)
for i in xrange(1, n):
    name = header[0]
    name2 = header[i]

    cloze_prob = select(table_probs, 0)
    prob = select(table_probs, i)
    cloze_prob, prob = filter_valid(cloze_prob, prob)
    # print sorted(cloze_prob, reverse=True)
    # print sorted(prob, reverse=True)
    # logit_plot(cloze_prob, prob, name, name2, "probabilities")

    # cloze_ppl = select(table_ppls, 0)
    # yppl = select(table_ppls, i)
    # plot(cloze_ppl, yppl, name, name2, "perplexity")
