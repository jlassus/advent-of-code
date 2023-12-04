import argparse
import importlib
import os
import sys
import time

def get_year_dirs(path):
    for entry in os.scandir(path):
        if entry.is_dir() and entry.name.isdecimal():
            yield entry

def get_latest_year_dir(path):
    return max(get_year_dirs(path), key=lambda e: int(e.name))

def get_module_function(module, part=None):
    func = None
    if part:
        func = getattr(module, 'f%s' % part, None)
    else:
        func = getattr(module, 'f2', None)
    if not func:
        func = getattr(module, 'f', None)
    if not func:
        func = getattr(module, 'f1', None)
    return func

def get_module_test_data(module, part=None):
    data = None
    if part:
        data = getattr(module, 'test%s' % part, None)
    if not data:
        data = getattr(module, 'test', None)
    if not data:
        data = getattr(module, 'test1', None)
    return data

def measure_performance(f):
    def measure(**kwargs):
        t0 = time.process_time_ns()
        result = f(**kwargs)
        t1 = time.process_time_ns()
        elapsed = t1 - t0
        if elapsed < 10_000_000:
            elapsed_str = '%d \u00b5s' % (elapsed // 1_000)
        elif elapsed < 10_000_000_000:
            elapsed_str = '%d ms' % (elapsed // 1_000_000)
        else:
            elapsed_str = '%d s' % (elapsed // 1_000_000_000)
        print('Elapsed time: %s' % elapsed_str)
        return result
    return measure

def parse_arguments():
    parser = argparse.ArgumentParser(prog='Advent of Code')
    parser.add_argument('day')
    parser.add_argument('-y', '--year')
    parser.add_argument('-p', '--part')
    parser.add_argument('-i', '--input')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

def read_input_file(path):
    with open(path) as f:
        return f.read()

def error(*args):
    print('\033[91m\033[1m', end='')
    print(*args, end='')
    print('\033[0m\033[0m')

def warn(*args):
    print('\033[93m\033[1m', end='')
    print(*args, end='')
    print('\033[0m\033[0m')

def main():
    args = parse_arguments()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if args.year:
        year_dir = os.path.join(base_dir, args.year)
        year = args.year
    else:
        year_dir = get_latest_year_dir(base_dir)
        year = year_dir.name
    try:
        module = importlib.import_module('%s.%s' % (year, args.day))
    except ModuleNotFoundError:
        error('Module not found: %s day %s' % (year, args.day))
        sys.exit(1)
    kwargs = {'debug': args.debug}
    func = get_module_function(module, args.part)
    if not func:
        error('No function found in module %s.%s' % (year, args.day))
        sys.exit(1)
    if len(func.__name__) > 1:
        args.part = func.__name__[-1]
    else:
        part = args.part
        if part.isdecimal():
            part = int(part)
        kwargs['part'] = part
    data = args.input
    if data is None:
        if args.test:
            data = get_module_test_data(module, args.part)
            if not data:
                warn('Warning: No test data found')
        else:
            input_path = os.path.join(year_dir, 'input', '%s.txt' % args.day)
            try:
                data = read_input_file(input_path)
            except FileNotFoundError:
                error('Input file not found:')
                print('  %s' % input_path)
                sys.exit(1)
    if data:
        data = data.strip().split('\n')
    kwargs['data'] = data
    print('%sing %s day %s %s(%s) with %d lines of data...' % ('Test' if args.test else 'Runn', year, args.day,
                                                               func.__name__, kwargs.get('part', ''), len(data)))
    func = measure_performance(func)
    result = func(**kwargs)
    print('Result:\n%s' % result)

if __name__ == '__main__':
    main()
