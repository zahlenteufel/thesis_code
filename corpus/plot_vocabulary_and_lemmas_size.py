import matplotlib.pyplot as plt


def get_growth_funcion_from_ascii_files(sample_interval=10):
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


def get_growth_funcion_from_factored_corpus_file(sample_interval=10):
    lemmas = set()
    words = set()
    word_count = 0
    result = []
    with open("factored_corpus_WGNCPL.txt") as f:
        for line in f:
            for word_bundle in line[:-1].split():
                fields = word_bundle.split(":")
                lemma = [field for field in fields if field.startswith("L-")][0][2:]
                words.add(fields[0])
                lemmas.add(lemma)
                if word_count % sample_interval == 0:
                    result.append((word_count, len(words), len(lemmas)))
                word_count += 1
    return result

if __name__ == "__main__":
    res = get_growth_funcion_from_factored_corpus_file(500)
    x, y, z = zip(*res)
    plt.close()
    line1, = plt.plot(x, y, "r")
    line2, = plt.plot(x, z, "b")
    plt.grid(True)
    plt.legend([line1, line2], ["tamano vocabulario", "tamano vocabulario de lemas"], loc=4)
    plt.show()
