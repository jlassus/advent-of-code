from collections import defaultdict

test = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

class Map:
    def __init__(self, maps=None):
        self.maps = maps or []

    def __add__(self, other):
        return self.merge(other)

    def translate(self, n):
        for m in self.maps:
            if n >= m[0] and n < m[0] + m[2]:
                return n + m[1] - m[0]
        return n

    def merge(self, other):
        # create a list 'finished'
        # for all other.maps
        #     for all self.maps
        #         add any parts in other map whose src does not overlap with self src into finished
        # add all self.maps into a list 'todo'
        # while we have maps left in todo, pop one map 'm'
        #     for all other.maps
        #         if m dst overlaps other src
        #             translate the part that overlaps
        #             if translated src and dst are equal, discard
        #             otherwise, add to finished
        #             any other sections (0-2) are added to todo
        #             break loop
        #     if no overlaps, add map to finished
        finished = []
        if isinstance(other, Map):
            other = other.maps
        for m1 in other:
            other_src_start = m1[0]
            other_src_stop = m1[0] + m1[2]
            other_translate_offset = m1[1] - m1[0]
            overlaps = []
            for m0 in self.maps:
                self_src_start = m0[0]
                self_src_stop = m0[0] + m0[2]
                if other_src_start < self_src_stop and other_src_stop > self_src_start:
                    overlap_start = max(self_src_start, other_src_start)
                    overlap_stop = min(self_src_stop, other_src_stop)
                    overlaps.append((overlap_start, overlap_stop))
            overlaps.sort(key=lambda o: o[0])
            prev_overlap_stop = other_src_start
            for overlap_start, overlap_stop in overlaps:
                distance_to_prev = overlap_start - prev_overlap_stop
                if distance_to_prev > 0:
                    finished.append((prev_overlap_stop, prev_overlap_stop + other_translate_offset, distance_to_prev))
                prev_overlap_stop = overlap_stop
            distance_to_prev = other_src_stop - prev_overlap_stop
            if distance_to_prev > 0:
                finished.append((prev_overlap_stop, prev_overlap_stop + other_translate_offset, distance_to_prev))
        todo = self.maps[:]
        while todo:
            m0 = todo.pop()
            self_src_start = m0[0]
            self_dst_start = m0[1]
            self_src_stop = m0[0] + m0[2]
            self_dst_stop = m0[1] + m0[2]
            self_translate_offset = m0[1] - m0[0]
            for m1 in other:
                other_src_start = m1[0]
                other_src_stop = m1[0] + m1[2]
                other_dst_start = m1[1]
                if other_src_start < self_dst_stop and other_src_stop > self_dst_start:
                    overlap_start = max(self_dst_start, other_src_start)
                    overlap_stop = min(self_dst_stop, other_src_stop)
                    overlap_length = overlap_stop - overlap_start
                    self_overlap_offset = overlap_start - self_dst_start
                    other_overlap_offset = overlap_start - other_src_start
                    translated_src_start = self_src_start + self_overlap_offset
                    translated_dst_start = other_dst_start + other_overlap_offset
                    if translated_src_start != translated_dst_start:
                        finished.append((translated_src_start, translated_dst_start, overlap_length))
                    if self_overlap_offset > 0:
                        todo.append((self_src_start, self_dst_start, self_overlap_offset))
                    translated_src_stop = translated_src_start + overlap_length
                    if translated_src_stop < self_src_stop:
                        todo.append((translated_src_stop, translated_src_stop + self_translate_offset, self_src_stop - translated_src_stop))
                    break
            else:
                finished.append(m0)
        return Map(finished)

def parse_maps(data):
    maps = defaultdict(dict)
    current_map = None
    for line in data:
        if line.endswith('map:'):
            source_map, dest_map = line[:-5].split('-to-')
            current_map = []
            maps[source_map][dest_map] = current_map
            continue
        elif not line or current_map is None:
            continue
        dst_start, src_start, n = line.split()
        current_map.append((int(src_start), int(dst_start), int(n)))
    return maps

def f(data, part, debug):
    seeds = [int(n) for n in data[0][7:].split()]
    assert len(seeds) & 1 == 0
    maps = parse_maps(data)
    combined_map = Map()
    map_steps = [
        maps['seed']['soil'],
        maps['soil']['fertilizer'],
        maps['fertilizer']['water'],
        maps['water']['light'],
        maps['light']['temperature'],
        maps['temperature']['humidity'],
        maps['humidity']['location'],
    ]
    for m in map_steps:
        combined_map += m
    closest = []
    if part == 1:
        for seed in seeds:
            closest.append(combined_map.translate(seed))
    else:
        for seed_start, seed_length in zip(seeds[0::2], seeds[1::2]):
            for m in combined_map.maps:
                if seed_start < m[0] + m[2] and seed_start + seed_length > m[0]:
                    closest.append(combined_map.translate(max(m[0], seed_start)))
    return min(closest)
