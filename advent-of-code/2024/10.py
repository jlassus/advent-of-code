test = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


directions = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def pre_process(data):
    rows = []
    w = 0
    h = len(data)
    for line in data:
        w = max(w, len(line))
        rows.append([int(v) for v in line])
    return rows, w, h


def get_highest_points(x, y, m, w, h):
    for dx, dy in directions:
        x1 = x + dx
        y1 = y + dy
        if x1 < 0 or x1 >= w or y1 < 0 or y1 >= h or m[y1][x1] != m[y][x] + 1:
            continue
        if m[y1][x1] == 9:
            yield x1, y1
        yield from get_highest_points(x1, y1, m, w, h)


def f(data, part, debug):
    m, w, h = pre_process(data)
    s = 0
    for y, row in enumerate(m):
        for x, v in enumerate(row):
            if v == 0:
                points = get_highest_points(x, y, m, w, h)
                score = len(list(points)) if part == 2 else len(set(points))
                s += score
    return s
