import itertools

test = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def f(data, part, debug):
    expand = 1 if part == 1 else 999_999
    empty_cols = []
    w = len(data[0])
    for col in range(w):
        for line in data:
            if line[col] != '.':
                break
        else:
            empty_cols.append(col)
    empty_rows = []
    for i, line in enumerate(data):
        if line.count('.') == w:
            empty_rows.append(i)
    positions = []
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c == '#':
                positions.append((col, row))
    s = 0
    for a, b in itertools.combinations(positions, 2):
        col_range = range(min(a[0], b[0]), max(a[0], b[0]))
        row_range = range(min(a[1], b[1]), max(a[1], b[1]))
        dist_x = len(col_range)
        dist_y = len(row_range)
        for e in empty_cols:
            if e in col_range:
                dist_x += expand
        for e in empty_rows:
            if e in row_range:
                dist_y += expand
        s += dist_x + dist_y
    return s
