import collections
import itertools


test = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def pre_process(data):
    m = collections.defaultdict(set)
    w = 0
    h = len(data)
    for y, line in enumerate(data):
        w = max(w, len(line))
        for x, c in enumerate(line):
            if c != '.':
                m[c].add((x, y))
    return m, w, h


def get_antinodes(a, b, w, h, part):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    if part == 2:
        yield a
        yield b
    for k, o in ((-1, a), (1, b)):
        i = 0
        while True:
            i += k
            if part == 1 and i in (-2, 2):
                break
            x = o[0] + dx * i
            y = o[1] + dy * i
            if x < 0 or x >= w or y < 0 or y >= h:
                break
            yield x, y


def f(data, part, debug):
    antinodes = set()
    m, w, h = pre_process(data)
    for positions in m.values():
        for a, b in itertools.combinations(positions, 2):
            antinodes = antinodes.union(get_antinodes(a, b, w, h, part))
    return len(antinodes)
