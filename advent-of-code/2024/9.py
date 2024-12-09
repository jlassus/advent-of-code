test = "2333133121414131402"


def pre_process(data):
    m = []
    p = 0
    for i, c in enumerate(data[0]):
        l = int(c)
        if i & 1:
            m.append(['E', p, l, None])
        else:
            m.append(['F', p, l, i >> 1])
        p += l
    return m


def visualize(m):
    s = []
    for a in m:
        if a[0] == 'E':
            s.extend('.' * a[2])
        else:
            s.extend(str(a[3]) * a[2])
    return ''.join(s)


def checksum(m):
    s = 0
    for a in m:
        if a[0] == 'F':
            for i in range(a[2]):
                s += (a[1] + i) * a[3]
    return s

def f1(data, debug):
    m = pre_process(data)
    if debug:
        print(visualize(m))
    pf = len(m) - 1
    pe = 1
    while True:
        if pf < pe:
            break
        f = m[pf]
        if f[0] != 'F':
            pf -= 1
            continue
        e = m[pe]
        if e[0] != 'E':
            pe += 1
            continue
        if e[2] >= f[2]:
            new_f = ['F', e[1], f[2], f[3]]
            del m[pf]
            if e[2] == f[2]:
                m[pe] = new_f
                pf -= 1
            else:
                m.insert(pe, new_f)
                e[1] += f[2]
                e[2] -= f[2]
            pe += 1
        else:
            m[pe] = ['F', e[1], e[2], f[3]]
            pe += 1
            f[2] -= e[2]
    if debug:
        print(visualize(m))
    return checksum(m)

def f2(data, debug):
    m = pre_process(data)
    if debug:
        print(visualize(m))
    pf = len(m) - 1
    while True:
        if pf < 1:
            break
        f = m[pf]
        if f[0] != 'F':
            pf -= 1
            continue
        for pe in range(0, pf):
            e = m[pe]
            if e[0] == 'E' and e[2] >= f[2]:
                f[1] = e[1]
                del m[pf]
                if e[2] == f[2]:
                    m[pe] = f
                    pf -= 1
                else:
                    m.insert(pe, f)
                    e[1] += f[2]
                    e[2] -= f[2]
                break
        else:
            pf -= 1
            continue
    if debug:
        print(visualize(m))
    return checksum(m)
