import collections

test = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

def pre_process(data):
    for line in data:
        left, right = line.split()
        yield int(left), int(right)

def f1(data, debug):
    left_list = []
    right_list = []
    for left, right in pre_process(data):
        left_list.append(left)
        right_list.append(right)
    left_list.sort()
    right_list.sort()
    return sum(abs(l - r) for l, r in zip(left_list, right_list))

def f2(data, debug):
    left_list = []
    right_dict = collections.defaultdict(int)
    for left, right in pre_process(data):
        left_list.append(left)
        right_dict[right] += 1
    return sum(l * right_dict[l] for l in left_list)
