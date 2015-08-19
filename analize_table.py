import matplotlib.pyplot as plt
from itertools import izip
from scipy.special import logit
from scipy.stats.stats import pearsonr
import math
import sys


def select(table, column):
    return [row[column] for row in table]


def filter_valid(x1, x2):
    return zip(*[(e1, e2) for e1, e2 in izip(x1, x2) if not math.isinf(e1) and not math.isinf(e2)])

row = header = sys.stdin.readline()[:-1].split()[1:]
table = []
while True:
    row = sys.stdin.readline()[:-1].split()
    if not row:
        break
    word, nums = row[0], map(float, row[1:])
    if all(map(lambda x: x >= 0 and not math.isinf(x), nums)):
        table.append(nums)
    else:
        print >>sys.stderr, word, nums

n = len(header)
for i in xrange(1, n):
    cloze_prob = logit(select(table, 0))
    y = logit(select(table, i))
    cloze_prob, y = filter_valid(cloze_prob, y)
    title = "logit %s vs. logit %s" % (header[0], header[i])
    plt.close()
    plt.xlabel("logit " + header[0])
    plt.ylabel("logit " + header[i])
    plt.scatter(cloze_prob, y, alpha=0.2)
    print pearsonr(cloze_prob, y)[0]
    plt.show()
