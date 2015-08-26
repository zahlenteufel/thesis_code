# eliminate unicode invisible characters, converting them to spaces
import io
import sys

stdin = io.open(sys.stdin.fileno(), encoding="utf-8")
stdout = io.open(sys.stdout.fileno(), encoding="utf-8")

hist = dict()

print >>sys.stderr, "populating histogram"

for line in stdin:
    for character in line[:-1]:
        hist[ord(character)] = hist.get(ord(character), 0) + 1

print >>sys.stderr, "hist populated"

L = sorted([(v, k) for k, v in hist.iteritems()], reverse=True)

for index, (count, letter) in enumerate(L):
    stdout.write(u"%d %c %s \"(%s)\\n" % (count, unichr(letter), unichr(letter).encode("ascii", "backslashreplace")))
