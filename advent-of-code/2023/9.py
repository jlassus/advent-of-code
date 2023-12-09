import itertools

test = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def predict(v, left=False):
    if sum(v) == 0:
        return 0
    diff = [b - a for a, b in itertools.pairwise(v)]
    d = predict(diff, left=left)
    if left:
        return v[0] - d
    return v[-1] + d

def f(data, part, debug):
    left = part == 2
    return sum((predict([int(n) for n in line.split()], left=left) for line in data))
