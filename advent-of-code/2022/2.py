test = """
A Y
B X
C Z
"""

def f(data, part, debug):
    score = 0
    for line in data:
        opponent, you = line.split()
        opponent = ord(opponent) - 65
        you = ord(you) - 88
        if part == 2:
            you = (opponent + you - 1) % 3
        score += ((1 - (opponent - you) % 3) % 3) * 3 + you + 1
    return score
