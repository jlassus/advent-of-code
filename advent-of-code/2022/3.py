test = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def get_priority(item):
    priority = ord(item)
    if priority > 96:
        return priority - 96
    return priority - 38

def f1(data, debug):
    priority_sum = 0
    for line in data:
        mid = len(line) >> 1
        compartment1 = set(line[:mid])
        compartment2 = set(line[mid:])
        item = (set(line[:mid]) & set(line[mid:])).pop()
        priority_sum += get_priority(item)
    return priority_sum

def f2(data, debug):
    priority_sum = 0
    group_count = len(data) // 3
    for group_num in range(group_count):
        line_num = group_num * 3
        item = (set(data[line_num]) & set(data[line_num + 1]) & set(data[line_num + 2])).pop()
        priority_sum += get_priority(item)
    return priority_sum
