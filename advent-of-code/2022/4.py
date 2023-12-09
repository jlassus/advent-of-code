test = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

def f(data, part, debug):
    overlap = 0
    for line in data:
        n = tuple(map(int, line.replace(',', '-', 1).split('-')))
        overlap += ((n[2] <= n[1] and n[3] >= n[0])
                    and (part == 2 or (n[2] >= n[0] and n[3] <= n[1]) or (n[0] >= n[2] and n[1] <= n[3])))
    return overlap
