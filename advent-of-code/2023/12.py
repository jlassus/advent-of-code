from functools import cache

test = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

@cache
def arrangements(sums, right):
    if not sums:
        return 1
    req = sum(sums) + len(sums) - 1
    free = len(right) - req
    if free < 0:
        return 0
    c = 0
    for offset in range(free + 1):
        if ('#' not in right[:offset]) and ('.' not in right[offset:offset + sums[0]]):
            if len(sums) == 1:
                if '#' in right[offset + sums[0]:]:
                    continue
            elif right[offset + sums[0]] == '#':
                continue
            c += arrangements(sums[1:], right[sums[0] + offset + 1:])
    return c

def f(data, part, debug):
    count = 0
    for n, line in enumerate(data, start=1):
        springs, sums = line.split()
        sums = tuple(int(s) for s in sums.split(','))
        if part == 2:
            springs = '?'.join((springs,) * 5)
            sums *= 5
        c = arrangements(sums, springs)
        count += c
        if debug:
            print('Line %d: %d' % (n, c))
    return count
