test = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def pre_process(data):
    sep = [i for i, line in enumerate(data) if not line]
    sep.append(len(data))
    locks = []
    keys = []
    start = 0
    for end in sep:
        device = [-1] * len(data[start])
        for i in range(start, end):
            for j in range(len(data[start])):
                device[j] += data[i][j] == '#'
        (keys if data[start][0] == '.' else locks).append(device)
        start = end + 1
    return locks, keys


def test_overlap(lock, key):
    return any(l + k > 5 for l, k in zip(lock, key))


def f1(data, debug):
    locks, keys = pre_process(data)
    count = 0
    for lock in locks:
        for key in keys:
            count += not test_overlap(lock, key)
    return count
