test = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

def f1(data, debug):
    valid_numbers = []
    invalid_numbers = []
    previous_numbers = []
    previous_symbols = []
    for line in data:
        numbers = []
        symbols = []
        number_start = -1
        for i, c in enumerate(line):
            if c.isnumeric():
                if number_start == -1:
                    number_start = i
            else:
                if number_start != -1:
                    numbers.append([int(line[number_start:i]), number_start, i - 1, 0])
                    number_start = -1
                if c != '.':
                    symbols.append(i)
        if number_start != -1:
            numbers.append([int(line[number_start:]), number_start, i, 0])
        for s in symbols + previous_symbols:
            for n in numbers + previous_numbers:
                if s >= n[1] - 1 and s <= n[2] + 1:
                    n[3] += 1
        for n in previous_numbers:
            if n[3]:
                valid_numbers.append(n)
            else:
                invalid_numbers.append(n)
        previous_numbers = numbers
        previous_symbols = symbols
    for n in previous_numbers:
        if n[3]:
            valid_numbers.append(n)
        else:
            invalid_numbers.append(n)
    if debug:
        print('\n'.join(str(v[0]) for v in valid_numbers))
    return sum(v[0] for v in valid_numbers)

def f2(data, debug):
    all_numbers = []
    all_gears = []
    for line in data:
        numbers = []
        gears = []
        number_start = -1
        for i, c in enumerate(line):
            if c.isnumeric():
                if number_start == -1:
                    number_start = i
            else:
                if number_start != -1:
                    numbers.append((int(line[number_start:i]), number_start, i - 1))
                    number_start = -1
                if c == '*':
                    gears.append(i)
        if number_start != -1:
            numbers.append((int(line[number_start:]), number_start, i))
        all_numbers.append(numbers)
        all_gears.append(gears)
    gear_sum = 0
    for line_num, gears in enumerate(all_gears):
        for gear in gears:
            found_parts = []
            parts = all_numbers[line_num]
            if line_num > 0:
                parts = parts + all_numbers[line_num - 1]
            if line_num < len(all_numbers) - 1:
                parts = parts + all_numbers[line_num + 1]
            for p in parts:
                if gear >= p[1] - 1 and gear <= p[2] + 1:
                    found_parts.append(p)
            if len(found_parts) == 2:
                s = found_parts[0][0] * found_parts[1][0]
                gear_sum += s
                if debug:
                    print(s)
    return gear_sum
