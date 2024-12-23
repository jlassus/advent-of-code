import collections
import functools

test = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def pre_process(data):
    edges = collections.defaultdict(set)
    for line in data:
        c0, c1 = line.split('-')
        edges[c0].add(c1)
        edges[c1].add(c0)
    return edges


def f1(data, debug):
    edges = pre_process(data)
    sets_of_three = set()
    for c0, others in edges.items():
        for c1 in others:
            for c2 in others & edges[c1]:
                s = tuple(sorted((c0, c1, c2)))
                if any(c[0] == 't' for c in s):
                    sets_of_three.add(s)
    return len(sets_of_three)


def f2(data, debug):
    edges = pre_process(data)
    @functools.cache
    def find_complete_graphs(s0):
        for c in s0:
            s1 = edges[c].intersection(s0)
            for graph in find_complete_graphs(tuple(sorted(s1))):
                yield (c,) + graph
            yield (c,)
    largest = ()
    for graph in find_complete_graphs(tuple(edges)):
        if len(graph) > len(largest):
            largest = graph
    return ','.join(sorted(largest))
