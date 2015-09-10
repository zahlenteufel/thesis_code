
class BackoffGraph():

    def __init__(self, parents):
        self.parents = map(
            lambda p: p.replace("(", "").replace(")", "").replace("-", ""),
            parents)
        self._order = 1 + max(map(lambda p: int(p[-1]), self.parents))
        self._factors = set(["W"] + [e[0] for e in self.parents])
        self.nodes = set([make_node(self.parents)])
        self.edges = set()

    def add_edge(self, line):
        if line.strip().split()[:2] == ["0", "0"]:
            return
        node_list, dropped_elements = line.split()[:2]
        node = make_node(node_list.split(","))
        dropped_elements = dropped_elements.split(",")
        for dropped_element in dropped_elements:
            new_node = take_out(node, dropped_element)
            self.nodes.add(new_node)
            self.edges.add((node, new_node))

    def visualize(self):
        "generates Graphviz code"
        nodes = list(self.nodes)
        s = 'digraph {\n  node[shape="box", style="rounded"];\n'
        for i, node in enumerate(nodes):
            s += '  %d [label="%s"];\n' % (i, ("W | " + node) if node else "W")
        for edge in self.edges:
            s += '  %d -> %d;\n' % tuple(map(nodes.index, edge))
        s += "}\n"
        return s

    def factors(self):
        return self._factors

    def order(self):
        return self._order


def make_node(elements):
    return ",".join(sorted(elements))


def take_out(node, element):
    node_elements = node.split(",")
    return make_node(e for e in node_elements if e != element)
