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
    s = (s ^ (s >> 5)) & 16777215
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
    monkeys = []
    for number in data:
        secret = int(number)
        p = secret % 10
        prices = [p]
        monkeys.append(prices)
        for _ in range(2000):
            secret = get_next_secret(secret)
            p1 = secret % 10
            prices.append(p1 - p)
            p = p1
    best = (0, None)
    try:
        for p0 in range(-9, 10):
            for p1 in range(-9, 10):
                for p2 in range(-9, 10):
                    for p3 in range(-9, 10):
                        total = 0
                        for prices in monkeys:
                            total += get_sell_price(prices, p0, p1, p2, p3)
                        if total > best[0]:
                            best = (total, (p0, p1, p2, p3))
                            print(f'New best: {total} ({p0}, {p1}, {p2}, {p3})')
    except KeyboardInterrupt:
        if best[1]:
            print(f'Best: {best[0]} ({best[1][0]}, {best[1][1]}, {best[1][2]}, {best[1][3]})')
    return best[0]
