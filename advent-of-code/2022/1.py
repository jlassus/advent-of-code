test = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def f(data, part, debug):
    calories_by_elf = []
    calories = 0
    for line in data:
        if not line:
            calories_by_elf.append(calories)
            calories = 0
            continue
        calories += int(line)
    calories_by_elf.append(calories)
    calories_by_elf.sort(reverse=True)
    if debug:
        print(calories_by_elf)
    if part == 1:
        return calories_by_elf[0]
    return sum(calories_by_elf[:3])