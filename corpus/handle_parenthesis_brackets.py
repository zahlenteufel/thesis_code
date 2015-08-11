#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import imap
import codecs
import sys
import re

sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


# class MockFile:
#     def __init__(self, str):
#         self.it = iter(str.split("\n"))

#     def readlines(self):
#         return self.it

# f = MockFile(u"""
#     «esto esta a medias....
#     «esto no», «esto si se imprime, joder!»
# """)

f = sys.stdin

MIN_ANGLES_INSIDE_NEWLINE = 3


def get_match_if_long_enough(mo):
    s = mo.string[mo.start():mo.end()][1:-1].split()
    if len(s) < MIN_ANGLES_INSIDE_NEWLINE:
        return " ".join(s)
    else:
        return ""


lines = imap(unicode.strip, f.readlines())
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
            print " ".join(words)
    line = regex_matched_parenthesis.sub("", line)
    for inside in regex_matched_angles.findall(line):
        words = inside.split()
        if len(words) >= MIN_ANGLES_INSIDE_NEWLINE:
            print " ".join(words)

    line = regex_matched_angles.sub(get_match_if_long_enough, line)
    if line:
        print line
