test = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

def f1(data, debug):
    total_points = 0
    for line in data:
        card, numbers = line.split(':')
        winning, own = numbers.split('|')
        winning = set(winning.split())
        own = set(own.split())
        points = len(winning & own)
        if points:
            points = 1 << (points -1)
        total_points += points
        if debug:
            print(points)
    return total_points

def f2(data, debug):
    copies = [1] * len(data)
    for i, line in enumerate(data):
        n = copies[i]
        card, numbers = line.split(':')
        winning, own = numbers.split('|')
        winning = set(winning.split())
        own = set(own.split())
        points = len(winning & own)
        for j in range(i + 1, i + 1 + points):
            copies[j] += n
    if debug:
        print('\n'.join(str(n) for n in copies))
    return sum(copies)
