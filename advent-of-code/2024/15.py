test = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


directions = {
    'v': (0, 1),
    '^': (0, -1),
    '>': (1, 0),
    '<': (-1, 0),
}


def pre_process(data, part):
    pos = None
    m = []
    lines = iter(data)
    for y, line in enumerate(lines):
        if not line:
            break
        if part == 2:
            line = line.replace('#', '##').replace('O', '[]').replace('.', '..').replace('@', '@.')
        if '@' in line:
            pos = line.index('@'), y
            line = line.replace('@', '.')
        m.append(list(line))
    moves = []
    for line in lines:
        moves.extend(line)
    return m, moves, pos


def move_box_rec(m, x0, y0, dx, dy, dry_run=False):
    c = m[y0][x0]
    if c == '.':
        return True
    if c == '#':
        return False
    if c == 'O' or not dy:
        x1 = x0 + dx
        y1 = y0 + dy
        if move_box_rec(m, x1, y1, dx, dy):
            m[y1][x1] = m[y0][x0]
            return True
        return False
    if dy:
        y1 = y0 + dy
        x1 = x0 + 1 if c == '[' else x0 - 1
        if (move_box_rec(m, x1, y1, 0, dy, dry_run=True)
            and move_box_rec(m, x0, y1, 0, dy, dry_run=dry_run)):
            if not dry_run:
                move_box_rec(m, x1, y1, 0, dy)
                m[y1][x0] = m[y0][x0]
                m[y1][x1] = m[y0][x1]
                m[y0][x0] = '.'
                m[y0][x1] = '.'
            return True
        return False


def f(data, part, debug):
    m, moves, (x0, y0) = pre_process(data, part)
    for move in moves:
        dx, dy = directions[move]
        x1 = x0 + dx
        y1 = y0 + dy
        if move_box_rec(m, x1, y1, dx, dy):
            m[y1][x1] = '.'
            x0, y0 = x1, y1
    b = '[' if part == 2 else 'O'
    s = 0
    for y, row in enumerate(m):
        for x, c in enumerate(row):
            if c == b:
                s += y * 100 + x
    return s
