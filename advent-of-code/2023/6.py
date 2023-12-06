import math

test = """
Time:      7  15   30
Distance:  9  40  200
"""

def get_speed(t, d):
    return (t - math.sqrt((t * t) - (d * 4))) * 0.5

def f(data, part, debug):
    times, distances = data
    times = times.split(maxsplit=1)[1]
    distances = distances.split(maxsplit=1)[1]
    if part == 1:
        times = [int(t) for t in times.split()]
        distances = [int(d) for d in distances.split()]
    else:
        times = [int(times.replace(' ', ''))]
        distances = [int(distances.replace(' ', ''))]
    margin = 1
    for t, d in zip(times, distances):
        s_low_float = get_speed(t, d)
        s_low = int(s_low_float + 1.0)
        s_high = t - s_low
        margin *= (s_high - s_low + 1)
    return margin
