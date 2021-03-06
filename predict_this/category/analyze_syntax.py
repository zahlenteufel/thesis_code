# -*- coding: utf-8 -*-
import subprocess
import more_itertools


def analyze(text):
    text = text.rstrip("\n") + "\n"
    freeling_output = call_freeling(text)
    return analyze_freeling_output(freeling_output)


def call_freeling(text):
    p = subprocess.Popen([
        "analyze",
        "-f", "/usr/local/share/freeling/config/es.cfg",
        "--nortk",
        "--nortkcon",
        "--nonumb",
        "--nocoref",
        "--noorto",
        "--nodate",
        "--nophon",
        "--noner",
        "--noloc",
        "--flush"],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE)
    assert u"¿" not in text and u"¡" not in text
    p.stdin.write(text.encode("utf-8"))
    result = p.communicate()[0].decode("utf-8")
    p.stdin.close()
    return result


def analyze_freeling_output(freeling_output):
    freeling_lines = more_itertools.peekable(freeling_output.split("\n"))
    while freeling_lines.peek():
        yield list(get_tagged_line(freeling_lines))


def get_tagged_line(freeling_output_line_peekable_iterator):
    while freeling_output_line_peekable_iterator.peek():
        line = freeling_output_line_peekable_iterator.next()
        if line == "":
            break
        word, lemma, description = parse_freeling_line(line)
        yield word, lemma.split("+")[0], description
    freeling_output_line_peekable_iterator.next()


def parse_freeling_line(line):
    assert "_" not in line
    return line.split()[:3]
