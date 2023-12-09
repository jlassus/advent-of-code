test = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

def f(data, part, debug):
    for i, line in enumerate(data):
        if not line:
            break
    empty = i
    stack_index = {n: i for i, n in enumerate(data[empty - 1].split())}
    stacks = [[] for _ in stack_index]
    letters = range(65, 91)
    for line in data[empty - 2::-1]:
        for i, c in enumerate(line):
            if ord(c) in letters:
                stacks[i >> 2].append(c)
    for line in data[empty + 1:]:
        line = line.split()
        count = int(line[1])
        src = stacks[stack_index[line[3]]]
        dst = stacks[stack_index[line[5]]]
        crates = src[-count:]
        del src[-count:]
        if part == 1:
            crates.reverse()
        dst.extend(crates)
    return ''.join(s[-1] for s in stacks)
