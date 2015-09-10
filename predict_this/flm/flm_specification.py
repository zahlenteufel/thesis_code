from ..category.category import parse_category_brief
from itertools import ifilter, imap, islice
from backoff_graph import BackoffGraph
from ..predictor.flm_predictor import FLM_Predictor


class FLM_Specification:

    def __init__(self, filename):
        with open(filename) as file:
            self._factor_file = filename
            lines = ifilter(
                _not(is_comment),
                imap(str.strip, file)
                )
            assert lines.next() == "1", "there must be only one model declaration in file"
            header = lines.next()
            self.parse_header(header)
            for line in islice(lines, self.num_backoff_edges):  # remaining lines..
                self.backoff_graph.add_edge(line)
            next_line = next(lines, None)
            assert next_line is None, "there should be no more uncommented lines: '%s'" % next_line

    def parse_header(self, h):
        fields = iter(h.split())
        assert fields.next() == "W"
        assert fields.next() == ":"
        self.num_parents = int(fields.next())
        self.backoff_graph = BackoffGraph(islice(fields, self.num_parents))
        self._count_file = fields.next()
        self._model_file = fields.next()
        self.num_backoff_edges = int(fields.next())

    def visualize(self):
        "generates graphviz's neato script, render with 'neato -n Tpng > image.png'"
        s = """digraph {
            node[style="filled", fillcolor="white", shape="circle", size="30,30", fixedsize=true]
            """
        n = self.order()
        for i in xrange(n):
            x = (n - i) * 100
            for j, factor in enumerate(self.factors()):
                y = (len(self.factors()) - j) * 100
                s += '%s%d [pos="%d,%d", label="%s%s"%s];\n' % (
                    factor.lower(),
                    i,
                    x,
                    y,
                    factor,
                    ("-%d" % i) if i > 0 else "",
                    ', fillcolor="gray"' if factor == "W" else ""
                    )
        for parent in self.backoff_graph.parents:
            s += parent.lower() + " -> w0;\n"
        s += "}\n"
        return s

    def factors(self):
        return self.backoff_graph.factors()

    def convert_to_flm_format(self, tagged_word):
        return ":".join([tagged_word.in_ascii()] + self.extract_factors(tagged_word))

    def extract_factors(self, tagged_word):
        category_code = tagged_word.category_code()
        info = reduce(extend, map(lambda c: parse_category_brief(c), category_code.split("+")), {})
        info["L"] = tagged_word.lemma()
        return ["%s-%s" % (key, value) for key, value in info.iteritems() if key in self.factors()]

    def predictor(self):
        return FLM_Predictor(self)

    def order(self):
        return self.backoff_graph.order()

    def model_file(self):
        return self._model_file

    def count_file(self):
        return self._count_file

    def factor_file(self):
        return self._factor_file


def extend(a, b):
    """Create a new dictionary with a's properties extended by b,
    without overwriting.

    >>> extend({'a':1,'b':2}, {'b':3,'c':4})
    {'a': 1, 'c': 4, 'b': 2}
    """
    return dict(b, **a)


def is_comment(s):
    return s.startswith("##")


def _not(f):
    return lambda x: not f(x)
