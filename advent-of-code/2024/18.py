import sys

test = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

if '-t' in sys.argv or '--test' in sys.argv:
    w = 7
    cutoff = 12
else:
    w = 71
    cutoff = 1024

nswe = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)

def pathfind(grid, start, goal):
    def heuristic(x, y):
        return abs(goal[0] - x) + abs(goal[1] - y)
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(*start)}
    while open_set:
        current = min(open_set, key=lambda n: (n not in f_score, f_score.get(n, 0)))
        if current == goal:
            return came_from
        open_set.remove(current)
        for d in nswe:
            neighbor = current[0] + d[0], current[1] + d[1]
            if neighbor in grid or neighbor[0] not in range(w) or neighbor[1] not in range(w):
                continue
            tentative_g_score = (current not in g_score, g_score.get(current, 0) + 1)
            if tentative_g_score < (neighbor not in g_score, g_score.get(neighbor, 0)):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score[1]
                f_score[neighbor] = tentative_g_score[1] + heuristic(*neighbor)
                open_set.add(neighbor)


def trace_path(path, start, goal):
    c = goal
    yield c
    while c != start:
        c = path[c]
        yield c


def f1(data, debug):
    grid = {tuple(map(int, line.split(','))) for line in data[:cutoff]}
    start = 0, 0
    goal = w - 1, w - 1
    path = pathfind(grid, start, goal)
    path = set(trace_path(path, start, goal))
    return len(path) - 1


def f2(data, debug):
    grid = {tuple(map(int, line.split(','))) for line in data[:cutoff]}
    start = 0, 0
    goal = w - 1, w - 1
    path = pathfind(grid, start, goal)
    path = set(trace_path(path, start, goal))
    for line in data[cutoff:]:
        p = tuple(map(int, line.split(',')))
        grid.add(p)
        if p in path:
            path = pathfind(grid, start, goal)
            if path is None:
                return '%d,%d' % p
            path = set(trace_path(path, start, goal))
