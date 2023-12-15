from collections import defaultdict

test = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""

def get_hash(s):
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h &= 255
    return h

class Box:
    def __init__(self):
        self.lenses = {}

    def add_lens(self, label, focal_len):
        existing = self.lenses.get(label)
        if existing:
            pos = existing[0]
        else:
            pos = len(self.lenses)
        self.lenses[label] = [pos, focal_len]

    def remove_lens(self, label):
        existing = self.lenses.get(label)
        if existing:
            del self.lenses[label]
            for lens in self.lenses.values():
                if lens[0] > existing[0]:
                    lens[0] -= 1

    def box_focusing_power(self):
        box_power = 0
        if len(self.lenses):
            box_number = get_hash(next(iter(self.lenses)))
            for pos, focal_len in self.lenses.values():
                box_power += ((box_number + 1) * (pos + 1) * focal_len)
        return box_power

def f1(data, debug):
    return sum(get_hash(step) for step in data[0].split(','))

def f2(data, debug):
    boxes = defaultdict(Box)
    for part in data[0].split(','):
        op = part.find('=')
        remove = False
        if op == -1:
            op = part.find('-')
            remove = True
        label = part[:op]
        box = boxes[get_hash(label)]
        if remove:
            box.remove_lens(label)
        else:
            focal_len = int(part[op + 1:])
            box.add_lens(label, focal_len)
    return sum(box.box_focusing_power() for box in boxes.values())
