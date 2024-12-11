import functools


test = "125 17"


@functools.cache
def simulate(n, steps):
    if steps == 0:
        return 1
    if n == 0:
        return simulate(1, steps - 1)
    else:
        s = str(n)
        if len(s) & 1 == 0:
            h = len(s) >> 1
            return simulate(int(s[:h]), steps - 1) + simulate(int(s[h:]), steps - 1)
        else:
            return simulate(n * 2024, steps - 1)


def f(data, part, debug):
    steps = 75 if part == 2 else 25
    stones = [int(n) for n in data[0].split()]
    return sum(simulate(v, steps) for v in stones)
