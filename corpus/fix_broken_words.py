from more_itertools import peekable
from itertools import ifilter, imap
import io
import sys

stdin = io.open(sys.stdin.fileno(), "r", encoding="utf-8")
stdout = io.open(sys.stdout.fileno(), "w", encoding="utf-8")

lines = peekable(ifilter(bool, imap(unicode.rstrip, stdin)))
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
            stdout.write(saved + line + "\n")
            saved = ""
if saved:
    stdout.write(saved + "\n")
