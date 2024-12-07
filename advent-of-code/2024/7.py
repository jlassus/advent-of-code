from collections import defaultdict
from operator import add, mul


test = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def pre_process(data):
    for line in data:
        output, inputs = line.split(': ')
        inputs = [int(v) for v in inputs.split()]
        yield int(output), inputs


def get_outputs_rec(values, ops, current=None):
    if not values:
        yield current
    elif current is None:
        yield from get_outputs_rec(values[1:], ops, current=values[0])
    else:
        for op in ops:
            yield from get_outputs_rec(values[1:], ops, current=op(current, values[0]))


def concat(a, b):
    return int(str(a) + str(b))


def f(data, part, debug):
    ops = [add, mul]
    if part == 2:
        ops.append(concat)
    total = 0
    for output, inputs in pre_process(data):
        for v in get_outputs_rec(inputs, ops):
            if v == output:
                total += output
                break
    return total
