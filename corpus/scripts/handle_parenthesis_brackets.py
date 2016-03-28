#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import imap
import re
import io
import sys

stdin = io.open(sys.stdin.fileno(), "r", encoding="utf-8")
stdout = io.open(sys.stdout.fileno(), "w", encoding="utf-8")


MIN_ANGLES_INSIDE_NEWLINE = 3


def get_match_if_long_enough(mo):
    s = mo.string[mo.start():mo.end()][1:-1].split()
    if len(s) < MIN_ANGLES_INSIDE_NEWLINE:
        return " ".join(s)
    else:
        return ""


lines = imap(unicode.strip, stdin)
saved = ""

regex_matched_brackets = re.compile(r"\[.*?\]")
regex_matched_parenthesis = re.compile(r"\(.*?\)")
regex_matched_angles = re.compile(ur"«(.*?)»")

buff_lines = []
for line in lines:
    line = regex_matched_brackets.sub("", line)
    for inside in regex_matched_parenthesis.findall(line):
        words = inside[1:-1].split()
        if len(words) >= MIN_ANGLES_INSIDE_NEWLINE:
            stdout.write(" ".join(words) + "\n")
    line = regex_matched_parenthesis.sub("", line)
    for inside in regex_matched_angles.findall(line):
        words = inside.split()
        if len(words) >= MIN_ANGLES_INSIDE_NEWLINE:
            stdout.write(" ".join(words) + "\n")

    line = regex_matched_angles.sub(get_match_if_long_enough, line)
    if line:
        stdout.write(line + "\n")
