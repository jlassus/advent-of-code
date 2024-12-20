test = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


nswe = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)


def pre_process(data):
    start = None
    end = None
    path = set()
    for y, line in enumerate(data):
        for x, c in enumerate(line):
            if c == '#':
                continue
            path.add((x, y))
            if c == 'S':
                start = x, y
            elif c == 'E':
                end = x, y
    return path, start, end


def pathfind(grid, w, h, start, goal):
    def heuristic(x, y):
        return abs(goal[0] - x) + abs(goal[1] - y)
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(*start)}
    while open_set:
        current = min(open_set, key=lambda n: (n not in f_score, f_score.get(n, 0)))
        if current == goal:
            return came_from, g_score
        open_set.remove(current)
        for d in nswe:
            neighbor = current[0] + d[0], current[1] + d[1]
            if neighbor not in grid or neighbor[0] not in range(w) or neighbor[1] not in range(h):
                continue
            tentative_g_score = (current not in g_score, g_score.get(current, 0) + 1)
            if tentative_g_score < (neighbor not in g_score, g_score.get(neighbor, 0)):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score[1]
                f_score[neighbor] = tentative_g_score[1] + heuristic(*neighbor)
                open_set.add(neighbor)


def trace_path(path, n):
    while n:
        yield n
        n = path.get(n)


def get_surrounding(n, max_dist):
    for dy in range(-max_dist, max_dist + 1):
        for dx in range(-max_dist, max_dist + 1):
            d = abs(dy) + abs(dx)
            if 0 < d <= max_dist:
                yield (n[0] + dx, n[1] + dy), d


def f(data, part, debug):
    h = len(data)
    w = len(data[0])
    path, start, goal = pre_process(data)
    came_from, scores = pathfind(path, w, h, start, goal)
    original_score = scores[goal]
    shortest = set(trace_path(came_from, goal))
    cheats = set()
    if debug:
        print('Original score: %d' % original_score)
    max_dist = 20 if part == 2 else 2
    for n0 in shortest:
        for n1, d in get_surrounding(n0, max_dist):
            if n1 in shortest:
                new_score = original_score - scores[n0] + scores[n1] + d
                if original_score - new_score >= 100:
                    cheats.add((n0, n1))
    return len(cheats)
