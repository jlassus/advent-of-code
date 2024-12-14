import sys


test = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

if '-t' in sys.argv or '--test' in sys.argv:
    w = 11
    h = 7
else:
    w = 101
    h = 103


def pre_process(data):
    for line in data:
        p, v = line.split()
        px, py = p[2:].split(',')
        vx, vy = v[2:].split(',')
        yield int(px), int(py), int(vx), int(vy)


def variance(distr):
    avg = sum(distr) / len(distr)
    return sum((n - avg) ** 2 for n in distr) / len(distr)


def visualize(grid):
    print('\n'.join(''.join('X' if n else ' ' for n in line) for line in grid))


def f1(data, debug):
    q1, q2, q3, q4 = 0, 0, 0, 0
    w2 = w // 2
    h2 = h // 2
    for px, py, vx, vy in pre_process(data):
        px = (px + vx * 100) % w
        py = (py + vy * 100) % h
        if px < w2:
            if py < h2:
                q1 += 1
            elif py > h2:
                q3 += 1
        elif px > w2:
            if py < h2:
                q2 += 1
            elif py > h2:
                q4 += 1
    return q1 * q2 * q3 * q4


def f2(data, debug):
    variance_threshold = 20
    robots = list(list(r) for r in pre_process(data))
    grid = [[0] * w for _ in range(h)]
    h_distr = [0] * w
    v_distr = [0] * h
    for r in robots:
        grid[r[1]][r[0]] += 1
        h_distr[r[0]] += 1
        v_distr[r[1]] += 1
    i = 0
    while True:
        i += 1
        for r in robots:
            grid[r[1]][r[0]] -= 1
            h_distr[r[0]] -= 1
            v_distr[r[1]] -= 1
            r[0] = (r[0] + r[2]) % w
            r[1] = (r[1] + r[3]) % h
            grid[r[1]][r[0]] += 1
            h_distr[r[0]] += 1
            v_distr[r[1]] += 1
        if variance(h_distr) > variance_threshold and variance(v_distr) > variance_threshold:
            visualize(grid)
            return i
