import bisect
import collections


test = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def pre_process(data):
    start = None
    rows = collections.defaultdict(list)
    columns = collections.defaultdict(list)
    w = 0
    h = len(data)
    directions = '^>v<'
    for y, line in enumerate(data):
        w = max(w, len(line))
        for x, c in enumerate(line):
            if c == '#':
                rows[y].append(x)
                columns[x].append(y)
            elif c in directions:
                if start:
                    raise ValueError('Multiple starting positions')
                start = (x, y, directions.index(c))
            elif c != '.':
                raise ValueError('Unknown character %r at (%d, %d)' % (c, x, y))
    if not start:
        raise ValueError('Missing start position')
    return start, rows, columns, w, h


def traverse(start, rows, columns, w, h):
    x0, y0, d = start
    yield start
    while True:
        if d == 0:
            y1 = next((y for y in reversed(columns[x0]) if y < y0), -1)
            for y in range(y0 - 1, y1, -1):
                yield x0, y, d
            if y1 == -1:
                break
            y0 = y1 + 1
        elif d == 1:
            x1 = next((x for x in rows[y0] if x > x0), w)
            for x in range(x0 + 1, x1):
                yield x, y0, d
            if x1 == w:
                break
            x0 = x1 - 1
        elif d == 2:
            y1 = next((y for y in columns[x0] if y > y0), h)
            for y in range(y0 + 1, y1):
                yield x0, y, d
            if y1 == h:
                break
            y0 = y1 - 1
        else:
            x1 = next((x for x in reversed(rows[y0]) if x < x0), -1)
            for x in range(x0 - 1, x1, -1):
                yield x, y0, d
            if x1 == -1:
                break
            x0 = x1 + 1
        d = (d + 1) % 4


def add_obstacle(rows, columns, x, y):
    bisect.insort(rows[y], x)
    bisect.insort(columns[x], y)


def remove_obstacle(rows, columns, x, y):
    rows[y].remove(x)
    columns[x].remove(y)


def has_loop(start, rows, columns, w, h):
    visited = set()
    for pos in traverse(start, rows, columns, w, h):
        if pos in visited:
            return True
        visited.add(pos)
    return False


def f1(data, debug):
    visited = set()
    for x, y, d in traverse(*pre_process(data)):
        visited.add((x, y))
    return len(visited)


def f2(data, debug):
    start, rows, columns, w, h = pre_process(data)
    obstacles = set()
    for x, y, d in traverse(start, rows, columns, w, h):
        if (x, y, d) == start or (x, y) in obstacles:
            continue
        if d == 0:
            try_obstacle = rows[y + 1] and rows[y + 1][-1] > x
        elif d == 1:
            try_obstacle = columns[x - 1] and columns[x - 1][-1] > y
        elif d == 2:
            try_obstacle = rows[y - 1] and rows[y - 1][0] < x
        else:
            try_obstacle = columns[x + 1] and columns[x + 1][0] < y
        if try_obstacle:
            add_obstacle(rows, columns, x, y)
            if has_loop(start, rows, columns, w, h):
                obstacles.add((x, y))
            remove_obstacle(rows, columns, x, y)
    return len(obstacles)
