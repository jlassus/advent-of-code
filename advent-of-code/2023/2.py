test = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

def f(data, part, debug):
    games = {}
    for line in data:
        game_id, line = line.split(':')
        game_id = int(game_id.split()[1])
        sets = line.split(';')
        sets_parsed = []
        games[game_id] = sets_parsed
        for s in sets:
            colors = (c.split() for c in s.split(','))
            colors = {c: int(n) for n, c in colors}
            sets_parsed.append(colors)
    if part == 1:
        possible = []
        for game_id, game in games.items():
            for s in game:
                if s.get('red', 0) > 12 or s.get('green', 0) > 13 or s.get('blue', 0) > 14:
                    break
            else:
                possible.append(game_id)
        if debug:
            print('\n'.join(str(n) for n in possible))
        return sum(possible)
    if part == 2:
        total = 0
        for game in games.values():
            r = g = b = 0
            for s in game:
                r = max(r, s.get('red', 0))
                g = max(g, s.get('green', 0))
                b = max(b, s.get('blue', 0))
            p = r * g * b
            total += p
            if debug:
                print(p)
        return total
