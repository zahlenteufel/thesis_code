from itertools import imap
import progressbar

progress_bar = progressbar.ProgressBar()
progress_bar.maxval = 10000
progress_bar.start()

def get_lemmas():
    for i in xrange(10000):
        progress_bar.update(i)
        with open("tagged_chunks/%s.ascii" % str(i).zfill(4)) as f:
            for line in f:
                if len(line) != 1:
                    lemmas = line.split()[1].split("_")
                    for lemma in lemmas:
                        yield lemma.split("+")[0]
    progress_bar.finish()


lemmas = get_lemmas()

def insert_lemma_as_factor(factors, lemma):
    f = factors.split(":")
    return ":".join(f[:1] + ["L-"+lemma] + f[1:])


with open("factored_corpus_WGNCP.txt") as fcorpus:
    with open("factored_corpus_WGNCPL.txt", "w") as result:
        for line in fcorpus:
            line = line[:-1]
            print >>result, " ".join(imap(insert_lemma_as_factor, line.split(), lemmas))
