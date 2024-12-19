import functools

test = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def has_solution(pattern, towels):
    if not pattern:
        return True
    for t in towels:
        if pattern.startswith(t) and has_solution(pattern[len(t):], towels):
            return True
    return False


@functools.cache
def count_solutions(pattern, towels):
    if not pattern:
        return 1
    c = 0
    for t in towels:
        if pattern.startswith(t):
            c += count_solutions(pattern[len(t):], towels)
    return c


def f(data, part, debug):
    towels = tuple(data[0].split(', '))
    patterns = data[2:]
    f = count_solutions if part == 2 else has_solution
    c = 0
    for pattern in patterns:
        c += f(pattern, towels)
    return c
