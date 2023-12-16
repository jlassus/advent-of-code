test = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

# right: 1, down: 2, left: 4, up: 8
rotations = {'/': {1: 8, 8: 1, 2: 4, 4: 2},
             '\\': {1: 2, 2: 1, 4: 8, 8: 4}}
splits = {'-': {2: (1, 4), 8: (1, 4)},
          '|': {1: (2, 8), 4: (2, 8)}}
rot_to_move = {1: (1, 0),
               2: (0, 1),
               4: (-1, 0),
               8: (0, -1)}

def simulate(data, beam_states):
    w = len(data[0])
    h = len(data)
    grid = [0] * (w * h)
    while beam_states:
        pos_x, pos_y, rot = beam_states.pop()
        while True:
            move_x, move_y = rot_to_move[rot]
            pos_x += move_x
            pos_y += move_y
            if pos_x < 0 or pos_x >= w or pos_y < 0 or pos_y >= h:
                break
            p = pos_x + pos_y * w
            if grid[p] & rot:
                break
            grid[p] |= rot
            c = data[pos_y][pos_x]
            if c in rotations:
                rot = rotations[c][rot]
            elif c in splits:
                split = splits[c].get(rot)
                if split:
                    rot = split[0]
                    beam_states.append((pos_x, pos_y, split[1]))
    return sum(bool(i) for i in grid)

def f1(data, debug):
    return simulate(data, [(-1, 0, 1)])

def f2(data, debug):
    w = len(data[0])
    h = len(data)
    energy_levels = []
    for x in range(w):
        energy_levels.append(simulate(data, [(x, -1, 2)]))
        energy_levels.append(simulate(data, [(x, h, 8)]))
    for y in range(h):
        energy_levels.append(simulate(data, [(-1, y, 1)]))
        energy_levels.append(simulate(data, [(w, y, 4)]))
    return max(energy_levels)
