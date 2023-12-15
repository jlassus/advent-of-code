test = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def tilt_north(data):
    h = len(data)
    w = len(data[0])
    for row in range(h):
        for col in range(w):
            if data[row][col] == 'O':
                for i in range(row - 1, -2, -1):
                    if i == -1 or data[i][col] != '.':
                        data[row][col] = '.'
                        data[i + 1][col] = 'O'
                        break

def tilt_south(data):
    h = len(data)
    w = len(data[0])
    for row in range(h - 1, -1, -1):
        for col in range(w):
            if data[row][col] == 'O':
                for i in range(row + 1, h + 1):
                    if i == h or data[i][col] != '.':
                        data[row][col] = '.'
                        data[i - 1][col] = 'O'
                        break

def tilt_east(data):
    h = len(data)
    w = len(data[0])
    for col in range(w - 1, -1, -1):
        for row in range(h):
            if data[row][col] == 'O':
                for i in range(col + 1, w + 1):
                    if i == w or data[row][i] != '.':
                        data[row][col] = '.'
                        data[row][i - 1] = 'O'
                        break

def tilt_west(data):
    h = len(data)
    w = len(data[0])
    for col in range(w):
        for row in range(h):
            if data[row][col] == 'O':
                for i in range(col - 1, -2, -1):
                    if i == -1 or data[row][i] != '.':
                        data[row][col] = '.'
                        data[row][i + 1] = 'O'
                        break

def f(data, part, debug):
    data = [list(line) for line in data]
    w = len(data[0])
    h = len(data)
    if part == 1:
        tilt_north(data)
    else:
        loop_lookup = {}
        config_lookup = {}
        cycles = 1_000_000_000
        for i in range(cycles):
            tilt_north(data)
            tilt_west(data)
            tilt_south(data)
            tilt_east(data)
            key = ''.join(''.join(row) for row in data)
            loop_start = loop_lookup.get(key)
            loop_lookup[key] = i
            config_lookup[i] = key
            if loop_start is not None:
                if debug:
                    print('Loop detected between %d and %d' % (loop_start, i))
                loop_len = i - loop_start
                config = config_lookup[i + ((cycles - i) % loop_len) - loop_len - 1]
                data = [config[j:j + w] for j in range(0, w * h, w)]
                break
    load = 0
    for row_i, row in enumerate(data):
        load += row.count('O') * (h - row_i)
    if debug:
        for row in data:
            print(''.join(row))
    return load
