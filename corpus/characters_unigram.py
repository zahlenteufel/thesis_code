# eliminate unicode invisible characters, converting them to spaces
# import unicodedata
import codecs
import sys

sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

hist = dict()

print >>sys.stderr, "populating histogram"

for l in sys.stdin.readlines():
    for c in l[:-1]:
        hist[ord(c)] = hist.get(ord(c), 0) + 1

print >>sys.stderr, "hist populated"

L = sorted([(v, k) for k, v in hist.iteritems()], reverse=True)

for index, (count, letter) in enumerate(L):
    print count, unichr(letter), "(%s)" % unichr(letter).encode("ascii", "backslashreplace")
