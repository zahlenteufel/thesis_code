import matplotlib.pyplot as plt
from scipy.special import logit


def plot_cols(colname1, colname2, file, logit_scale=False):
    with open(file) as f:
        header = f.readline()[:-1].split(",")
    plot(header.index(colname1), header.index(colname2), file, logit_scale)


def plot(ind1, ind2, file, logit_scale=False):
    f = open(file)

    header = f.readline()[:-1].split(",")
    x = []
    y = []

    for i, line in enumerate(f.readlines()):
        fields = line[:-1].split(",")
        x.append(float(fields[ind1]))
        y.append(float(fields[ind2]))

    if logit_scale:
        x = logit(x)
        y = logit(y)
    plt.xlabel(header[ind1] + ("(logit)" if logit_scale else ""))
    plt.ylabel(header[ind2] + ("(logit)" if logit_scale else ""))
    plt.scatter(x, y, alpha=0.05)
    plt.show()

plot_cols("entropia_4gram", "prob_4gram", "analisis_4gram_2.csv", logit_scale=False)
plt.close()
