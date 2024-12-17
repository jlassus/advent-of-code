test1 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

test2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


def pre_process(data):
    reg = {}
    lines = iter(data)
    for line in lines:
        if not line:
            break
        reg[line[9]] = int(line[12:])
    program = [int(i) for i in next(lines).split()[1].split(',')]
    return reg, program


def compute(reg, program):
    instr_ptr = 0
    l = len(program)
    step = -1
    abort = 1_000_000
    while instr_ptr < l:
        step += 1
        if step == abort:
            print(reg)
            print('Abort')
            return
        instr = program[instr_ptr]
        op = program[instr_ptr + 1]
        c_op = op if op < 4 else reg[chr(op + 61)]
        match instr:
            case 0:  # adv (division)
                reg['A'] //= (1 << c_op)
            case 1:  # bxl (xor)
                reg['B'] ^= op
            case 2:  # bst (mod 8)
                reg['B'] = c_op & 7
            case 3:  # jnz (jump)
                if reg['A']:
                    instr_ptr = op
                    continue
            case 4:  # bxc (xor)
                reg['B'] ^= reg['C']
            case 5:  # out (mod 8)
                yield c_op & 7
            case 6:  # bdv (division)
                reg['B'] = reg['A'] // (1 << c_op)
            case 7:  # cdv (division)
                reg['C'] = reg['A'] // (1 << c_op)
        instr_ptr += 2


def f1(data, debug):
    reg, program = pre_process(data)
    return ','.join(str(n) for n in compute(reg, program))


# New best: 13 (A = 1252799368813)
# New best: 14 (A = 10048892391021)
# New best: 15 (A = 95810799357549)

#       10010001110110000101010010100111001101101
#    10010010001110110000101010010100111001101101
# 10101110010001110110000101010010100111001101101
#       10010001110110000101010010100111001101101  # 1252799368813
#      100000000000000000000000000000000000000000  # 2199023255552

def f2(data, debug):
    reg, program = pre_process(data)
    l = len(program)
    i = 1252799368813
    best = (0, -1)
    n = 0
    try:
        while True:
            reg['A'] = i
            reg['B'] = 0
            reg['C'] = 0
            for n, o in enumerate(compute(reg, program)):
                if n == l or o != program[n]:
                    break
            else:
                if n == l - 1:
                    return i
            if n > best[0]:
                print('New best: %d (A = %d)' % (n, i))
                best = (n, i)
            i += 2199023255552
    except KeyboardInterrupt:
        print('Best: %d (A = %d)' % best)
