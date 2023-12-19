import functools
import itertools
import operator

test = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

class Cube:
    def __init__(self, pos, size):
        pos = tuple(pos)
        size = tuple(max(0, s) for s in size)
        self.dim = len(pos)
        if len(size) != self.dim:
            raise ValueError('Inconsistent number of dimensions')
        self.pos = pos
        self.size = size
        self.hash = hash((pos, size))

    @property
    def volume(self):
        return functools.reduce(operator.mul, self.size)

    def __repr__(self):
        return 'Cube(pos=%s, size=%s)' % (repr(self.pos), repr(self.size))

    def __hash__(self):
        return self.hash

    def __and__(self, other):
        if self.dim != other.dim:
            raise ValueError('Inconsistent number of dimensions')
        pos = []
        size = []
        for i in range(self.dim):
            d0 = max(self.pos[i], other.pos[i])
            d1 = min(self.pos[i] + self.size[i], other.pos[i] + other.size[i])
            pos.append(d0)
            size.append(d1 - d0)
        return Cube(pos, size)

def get_workflows(lines):
    workflows = {}
    for workflow in lines:
        if not workflow:
            break
        name, wf = workflow.split('{', 1)
        wf = wf[:-1].split(',')
        rules = []
        workflows[name] = rules
        for rule in wf:
            if ':' in rule:
                rule, target = rule.split(':')
                var = rule[0]
                op = rule[1]
                n = int(rule[2:])
                rules.append((var, op, n, target))
            else:
                rules.append((None, None, None, rule))
    return workflows

def f1(data, debug):
    lines = iter(data)
    workflows = get_workflows(lines)
    comparisons = {'<': operator.lt, '>': operator.gt}
    accepted = []
    for part in lines:
        part = part[1:-1]
        properties = part.split(',')
        p = {k: int(v) for k, v in (prop.split('=', 1) for prop in properties)}
        wf = 'in'
        while wf not in ('A', 'R'):
            for r in workflows[wf]:
                if r[0] is None or comparisons[r[1]](p[r[0]], r[2]):
                    wf = r[3]
                    break
        if wf == 'A':
            accepted.append(p)
    s = 0
    for part in accepted:
        s += sum(part.values())
    return s

def f2(data, debug):
    workflows = get_workflows(data)
    cubes = set()
    var_index = {c: i for i, c in enumerate('xmas')}

    def get_cubes(wf_id, cube):
        if wf_id == 'A':
            cubes.add(cube)
            return
        elif wf_id == 'R':
            return
        for rule in workflows[wf_id]:
            if rule[0] is not None:
                p = [1, 1, 1, 1]
                s = [4000, 4000, 4000, 4000]
                var_i = var_index[rule[0]]
                n = rule[2]
                if rule[1] == '<':
                    s[var_i] = n - 1
                    c0 = Cube(p, s)
                    p[var_i] = n
                    s[var_i] = 4001 - n
                    c1 = Cube(p, s)
                else:
                    s[var_i] = n
                    c1 = Cube(p, s)
                    p[var_i] = n + 1
                    s[var_i] = 4000 - n
                    c0 = Cube(p, s)
                get_cubes(rule[3], cube & c0)
                cube &= c1
            else:
                get_cubes(rule[3], cube)
    get_cubes('in', Cube((1, 1, 1, 1), (4000, 4000, 4000, 4000)))
    volume = 0
    i = 1
    while True:
        stop = True
        for c in itertools.combinations(cubes, i):
            overlap = functools.reduce(operator.and_, c)
            v = overlap.volume
            if v:
                stop = False
                if i & 1:
                    volume += v
                else:
                    volume -= v
        i += 1
        if stop:
            break
    return volume
