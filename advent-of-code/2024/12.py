import collections


test = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def pre_process(data):
    plots = collections.defaultdict(list)
    width_range = range(len(data[0]))
    height_range = range(len(data))
    for y, row in enumerate(data):
        for x, t in enumerate(row):
            neighbors = ((x + d[0], y + d[1]) for d in directions)
            neighbors = {n for n in neighbors if n[0] in width_range and n[1] in height_range
                                                 and data[n[1]][n[0]] == t}
            intersects = []
            for plts in plots[t]:
                if plts.intersection(neighbors):
                    intersects.append(plts)
            if len(intersects) > 1:
                plots[t] = [p for p in plots[t] if p not in intersects]
                plots[t].append(intersects[0])
                intersects[0].update(*intersects[1:])
                intersects[0].add((x, y))
            elif len(intersects) == 1:
                intersects[0].add((x, y))
            else:
                plots[t].append({(x, y)})
    for plot_type in plots.values():
        yield from plot_type


def f1(data, debug):
    s = 0
    for plot in pre_process(data):
        perim = 0
        for x, y in plot:
            for d in directions:
                if (x + d[0], y + d[1]) not in plot:
                    perim += 1
        s += len(plot) * perim
    return s


def f2(data, debug):
    s = 0
    for plot in pre_process(data):
        corners = 0
        for x, y in plot:
            if (x, y + 1) in plot:
                if (x + 1, y) in plot and (x + 1, y + 1) not in plot:
                    corners += 1
                if (x - 1, y) in plot and (x - 1, y + 1) not in plot:
                    corners += 1
            else:
                if (x + 1, y) not in plot:
                    corners += 1
                if (x - 1, y) not in plot:
                    corners += 1
            if (x, y - 1) in plot:
                if (x + 1, y) in plot and (x + 1, y - 1) not in plot:
                    corners += 1
                if (x - 1, y) in plot and (x - 1, y - 1) not in plot:
                    corners += 1
            else:
                if (x + 1, y) not in plot:
                    corners += 1
                if (x - 1, y) not in plot:
                    corners += 1
        s += len(plot) * corners
    return s
