from more_itertools import peekable
from itertools import ifilter, imap
import codecs
import sys

sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


# class MockFile:
#     def __init__(self, str):
#         self.it = iter(str.split("\n"))

#     def readlines(self):
#         return self.it

f = sys.stdin

lines = peekable(ifilter(bool, imap(unicode.rstrip, f.readlines())))
saved = ""

for line in lines:
    line = line.rstrip()

    if line:
        if len(line) > 2 and \
                line[-2] != " " and \
                line[-1] == "-" and \
                "-" not in line[:-1] and \
                not (lines.peek("a") or "a")[0].isupper():
            saved += line[:-1]
        else:
            print saved + line
            saved = ""
if saved:
    print saved
