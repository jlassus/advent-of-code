import math

test1 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

test2 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def steps_until_z(node, network, instructions):
    step = 0
    lr_index = {'L': 0, 'R': 1}
    while node[-1] != 'Z':
        lr = lr_index[instructions[step % len(instructions)]]
        node = network[node][lr]
        step += 1
    return step

def f(data, part, debug):
    instructions = data[0]
    network = {line[0:3]: (line[7:10], line[12:15]) for line in data[2:]}
    if part == 1:
        return steps_until_z('AAA', network, instructions)
    return math.lcm(*(steps_until_z(n, network, instructions) for n in network if n[-1] == 'A'))
