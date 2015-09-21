import matplotlib.pyplot as plt


def get_growth_funcion(sample_interval=10):
    lemmas = set()
    words = set()
    word_count = 0
    result = []
    for i in xrange(10000):
        with open("tagged_chunks/%s.ascii" % str(i).zfill(4)) as f:
            for line in f:
                if len(line) != 1:
                    if word_count % sample_interval == 0:
                        result.append((word_count, len(words), len(lemmas)))
                    line_words = line.split()[0].split("_")
                    line_lemmas = line.split()[1].split("_")
                    for word in line_words:
                        words.add(word)
                        word_count += 1
                    for lemma in line_lemmas:
                        lemmas.add(lemma.split("+")[0])
    return result

if __name__ == "__main__":
    res = get_growth_funcion(100)
    x, y, z = zip(*res)

plt.close()
line1, = plt.semilogy(x, y, "r")
line2, = plt.semilogy(x, z, "b")
plt.grid(True)
plt.legend([line1, line2], ["tamano vocabulario", "tamano vocabulario de lemas"], loc=4)
plt.show()
