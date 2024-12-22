import collections

test1 = """
1
10
100
2024
"""

test2 = """
1
2
3
2024
"""


def get_next_secret(s):
    s = (s ^ (s << 6)) & 16777215
    s = (s ^ (s >> 5))
    s = (s ^ (s << 11)) & 16777215
    return s


def get_sell_price(prices, p0, p1, p2, p3):
    total = 0
    for i, p in enumerate(prices):
        total += p
        if p == p3 and i > 3 and prices[i - 1] == p2 and prices[i - 2] == p1 and prices[i - 3] == p0:
            return total
    return 0


def f1(data, debug):
    s = 0
    for number in data:
        secret = int(number)
        for _ in range(2000):
            secret = get_next_secret(secret)
        s += secret
    return s


def f2(data, debug):
    sequences = collections.Counter()
    differences = collections.deque(maxlen=4)
    seen = set()
    for number in data:
        secret = int(number)
        p0 = secret % 10
        for _ in range(2000):
            secret = get_next_secret(secret)
            p1 = secret % 10
            differences.append(p1 - p0)
            seq = tuple(differences)
            if seq not in seen and len(seq) == 4:
                seen.add(seq)
                sequences[seq] += p1
            p0 = p1
        differences.clear()
        seen.clear()
    return max(sequences.values())
