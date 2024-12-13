test = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def pre_process(data):
    machine = {}
    for line in data:
        if not line:
            yield machine
            machine = {}
            continue
        key, value = line.split(': ')
        x, y = value.split(', ')
        if key.startswith('Button '):
            key = key.split()[1].lower()
        else:
            key = 'p'
        machine[key] = (int(x[2:]), int(y[2:]))
    yield machine


def get_presses(ax, ay, bx, by, px, py):
    a = (px*by - py*bx) / (ax*by - ay*bx)
    b = (py - a * ay) / by
    an = int(a)
    bn = int(b)
    if an != a or bn != b:
        return None
    return an, bn


def f(data, part, debug):
    total = 0
    N = 10_000_000_000_000
    for m in pre_process(data):
        px, py = m['p']
        if part == 2:
            px += N
            py += N
        presses = get_presses(*m['a'], *m['b'], px, py)
        if presses:
            a, b = presses
            total += a * 3 + b
    return total
