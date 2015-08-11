#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys

sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

replace_dict = {
    u"\x0c": u" ",
    u"\xad": u" ",
    u"…": u"\n",   # create new line..
    u"―": u"\n",   # create new line..
    u"": u"\n",  # create new line..
    u"ｭ": u"\n",   # create new line..
    u"Ώ": u"\n",   # create new line..
    u"΅": u"\n",   # create new line..
    u"−": u"\n",
    u"⇒": u"\n",
    u"σ": u"ó",
    u"ν": u"í",
    u"#": u"",
    u"α": u"á",
    u"ι": u"é",
    u"у": u"ó",  # it's a unicode greek letter, not a Y
    u"н": u"í",
    u"‡": u"á",
    u"ρ": u"ñ",
    u"б": u"á",
    u"+": u"",
    u"й": u"é",
    u"ϊ": u"ú",
    u"$": u"",
    u"─": u"ñ",
    u"–": u"ñ",
    u"с": u"ñ",
    u"œ": u"ú",
    u"ъ": u"ú",
    u"†": u"",
    u"ο": u"",
    u"Ι": u"É",
    u"ψ": u"psi",
    u"ε": u"",
    u"η": u"",
    u"τ": u"",
    u"ϕ": u"phi",
    u"π": u"pi",
    u"ί": u"",
    u"ς": u"",
    u"μ": u"Á",
    u"δ": u"",
    u"ό": u"ü",
    u"æ": u"ae",
    u"Β": u"",
    u"": u"",
    u"ø": u"o",
    u"‚": u"e",
    u"Α": u"a",
    u"Æ": u"ae",
    u"&": u"",
    u"\t": u"",
    u"_": u"",
}

for l in sys.stdin.readlines():
    s = u""
    for c in l[:-1]:
        s += replace_dict.get(c, c)
    print s
