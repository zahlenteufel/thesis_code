import unicodedata
import subprocess
from itertools import izip
import xmlrpclib
import time
import json
import os
import srilm
import sys
import csv
import target_word
from unigram_predictor import UnigramPredictor


def my_env(s):
    env = {
        "CORPUS_FILE": "corpus_limpio.txt",
        "CORPUS_PATH": "/home/gas/Desktop/tesis/corpus",
        "PLOTS_PATH": "/home/gas/Desktop/tesis/plots",
        "PREDICTIONS_PATH": "/home/gas/Desktop/tesis/predictions"
    }
    if s not in os.environ:
        return env[s]
    else:
        return os.environ[s]


def text_info(id):
    with open(my_env("CORPUS_PATH") + "/texts/metadata.json") as metadata_file:
        FULL_TEXT_INFO = json.load(metadata_file)
        return FULL_TEXT_INFO[str(id)]


def get_predictor_client():
    # is server running?
    try:
        subprocess.check_call(["lsof", "-i:9999"])
    except subprocess.CalledProcessError:
        # launch server..
        subprocess.Popen(["python", "ngram_server.py"])
        info("sleeping to give time to the server to load the model... zzz")
        time.sleep(60)
    return xmlrpclib.ServerProxy("http://localhost:9999")


def get_working_model(MAX_ORDER):
    info("loading model (this may take some time...)")

    vocab = srilm.vocab.Vocab()
    vocab.read(my_env("CORPUS_PATH") + "/vocabulario.txt")

    model = srilm.ngram.Lm(vocab, MAX_ORDER)
    model.read(my_env("CORPUS_PATH") + "/7-gram_model.srilm.gz")

    info("done")
    return model, vocab


def info(s):
    print >>sys.stderr, s


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return izip(*args)


def invert(d):
    return dict((v, [k for k, v2 in d.iteritems() if v2 == v]) for v in d.values())


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii


def formatear(s):
    return "".join(map(formatearLetra, s))


def formatearLetra(l):
    l = remove_accents(l)
    return l.lower()


def simpl(s):
    return unicode(s, 'Latin-1')


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_table(text_number):
    with open(my_env("CORPUS_PATH") + "/texts/texts1234578.csv") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        return [row for row in reader if int(row['indtexto']) == text_number]


def read_palabras(text_number):
    return " ".join([row['palabras'] for row in read_table(text_number)])


def is_initial(row):
    return row['palabras'][0].isupper() and row['CM_catsimple'] != 'n'


def get_text_targets(text_number, max_order):
    unigram_cache = UnigramPredictor()
    text = []
    targets = []
    for row in read_table(text_number):
        if is_initial(row):
            text.append("<s>")
        simplified_word = formatear(simpl(row['palabras']))
        if row['palabrascompletadas']:
            if max_order == 1:
                context = []
            else:
                i = 1
                while i <= len(text) and i < max_order - 1 and text[-i] != "<s>":
                    i += 1
                context = text[-i:]
            targets.append(
                target_word.TargetWord(
                    target_index=len(targets),
                    text_number=text_number,
                    text_index=len(text),
                    context=context,
                    row=row,
                    cache_unigram_prob=unigram_cache.prob(simplified_word)
                )
            )
        text.append(simplified_word)
        unigram_cache.add(simplified_word)
    return text, targets
