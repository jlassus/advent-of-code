numbers_spelled = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

test1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

test2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

def f1(data, debug):
    numbers = []
    for line in data:
        first = last = None
        for c in line:
            if c.isnumeric():
                if first is None:
                    first = c
                last = c
        n = int(first + last)
        numbers.append(n)
    if debug:
        print('\n'.join(str(n) for n in numbers))
    return sum(numbers)

def f2(data, debug):
    numbers = []
    for line in data:
        line_numbers = []
        for i, c in enumerate(line):
            if c.isnumeric():
                line_numbers.append(c)
            else:
                for j, n in enumerate(numbers_spelled):
                    if i + 1 >= len(n) and line[i + 1 - len(n):i + 1] == n:
                        line_numbers.append(str(j + 1))
        if line_numbers:
            numbers.append(int(line_numbers[0] + line_numbers[-1]))
    if debug:
        print('\n'.join(str(n) for n in numbers))
    return sum(numbers)
