import functools


test = """
029A
980A
179A
456A
379A
"""

nswe = {
    (0, -1): '^',
    (0, 1): 'v',
    (-1, 0): '<',
    (1, 0): '>',
}
pad1_key_to_pos = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}
pad2_key_to_pos = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}
pad1_pos_to_key = {pos: key for key, pos in pad1_key_to_pos.items()}
pad2_pos_to_key = {pos: key for key, pos in pad2_key_to_pos.items()}


def add_coordinates(pos0, pos1):
    return pos0[0] + pos1[0], pos0[1] + pos1[1]


def manhattan(pos0, pos1):
    return abs(pos1[0] - pos0[0]) + abs(pos1[1] - pos0[1])


@functools.cache
def get_steps(state, target, robot_count):
    if not state:
        return state, 1
    current = state[0]
    if current == target:
        state1, steps = get_steps(state[1:], 'A', robot_count)
        return (state[0],) + state1, steps
    if len(state) == robot_count:
        key_to_pos, pos_to_key = pad1_key_to_pos, pad1_pos_to_key
    else:
        key_to_pos, pos_to_key = pad2_key_to_pos, pad2_pos_to_key
    current_pos = key_to_pos[current]
    target_pos = key_to_pos[target]
    dist = manhattan(current_pos, target_pos)
    candidates = []
    for d, k in nswe.items():
        pos = add_coordinates(current_pos, d)
        if pos in pos_to_key and manhattan(pos, target_pos) < dist:
            state1, steps = get_steps(state[1:], k, robot_count)
            state1, steps1 = get_steps((pos_to_key[pos],) + state1, target, robot_count)
            candidates.append((state1, steps + steps1))
    return min(candidates, key=lambda v: v[1])


def f(data, part, debug):
    c = 0
    state = ('A',) * (26 if part == 2 else 3)
    for code in data:
        steps = 0
        for btn in code:
            state, steps1 = get_steps(state, btn, len(state))
            steps += steps1
        c += steps * int(code[:-1])
    return c
