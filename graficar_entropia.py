import matplotlib.pyplot as plt


def plot_cols(colname1, colname2, file):
    with open(file) as f:
        header = f.readline()[:-1].split(",")
    plot(header.index(colname1), header.index(colname2), file)


def plot(ind1, ind2, file):
    f = open(file)

    header = f.readline()[:-1].split(",")
    x = []
    y = []

    for i, line in enumerate(f.readlines()):
        fields = line[:-1].split(",")
        # print i, fields
        x.append(float(fields[ind1]))
        y.append(float(fields[ind2]))

    plt.xlabel(header[ind1])
    plt.ylabel(header[ind2])
    plt.scatter(x, y)
    plt.show()

# texto,#palabra,palabra,cloze_entropy,zeros,2gram_entropy,#texto,#palabra,
# palabra,prob_cloze,prob_cache,prob2gram

#texto,#palabra,palabra,cloze_predictor,unigram_cache_predictor,4gram

# plot_cols("cloze_predictor", "prob_cloze", "entropias")
plot(1, 0, "prob_ent4.csv")
plt.close()
