test = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

def f(data, part, debug):
    directions = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    x, y = 0, 0
    up_walls = []
    down_walls = []
    horizontal_walls = {}
    for line in data:
        d, n, color = line.split()
        if part == 1:
            d = directions[d]
            n = int(n)
        else:
            n = int(color[2:-2], 16)
            d = int(color[-2:-1])
        if d == 0:
            horizontal_walls[(x, y)] = x + n
            horizontal_walls[(x + n, y)] = x
            x += n
        elif d == 1:
            down_walls.append((x, y, y + n))
            y += n
        elif d == 2:
            horizontal_walls[(x, y)] = x - n
            horizontal_walls[(x - n, y)] = x
            x -= n
        else:
            up_walls.append((x, y - n, y))
            y -= n
    up_walls.sort(key=lambda w: w[0])
    down_walls.sort(key=lambda w: w[0])
    if up_walls[0][0] < down_walls[0][0]:
        start_walls = up_walls
        end_walls = down_walls
    else:
        start_walls = down_walls
        end_walls = up_walls
    area = 0
    for swx, sw0, sw1 in start_walls:
        if horizontal_walls[(swx, sw0)] < swx:
            sw0 += 1
        if horizontal_walls[(swx, sw1)] < swx:
            sw1 -= 1
        sections = [(sw0, sw1)]
        for ewx, ew0, ew1 in end_walls:
            if ewx <= swx:
                continue
            if horizontal_walls[(ewx, ew0)] > ewx:
                ew0 += 1
            if horizontal_walls[(ewx, ew1)] > ewx:
                ew1 -= 1
            i = 0
            for s0, s1 in tuple(sections):
                overlap_start = max(s0, ew0)
                overlap_end = min(s1, ew1)
                overlap_size = overlap_end - overlap_start + 1
                if overlap_size <= 0:
                    i += 1
                    continue
                area += (overlap_size * (ewx - swx + 1))
                del sections[i]
                if overlap_start > s0:
                    sections.append((s0, overlap_start - 1))
                if overlap_end < s1:
                    sections.append((overlap_end + 1, s1))
                if not sections:
                    break
    return area
