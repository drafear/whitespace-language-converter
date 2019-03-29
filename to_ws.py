import sys
import os
import re
import argparse

def parseargs():
    parser = argparse.ArgumentParser(
        description='convert Our Language to Whitespace')
    parser.add_argument('input', type=str,
                        help='input source file name')
    parser.add_argument('--output', '-o', type=str,
                        help='output whitespace file name')
    return parser.parse_args()

def is_int(n: str):
    return re.compile(r'^(0|-?[1-9]\d*)$').match(n) is not None

def to_bin(n: int):
    if n == 0:
        return '0'
    if n > 0:
        return '0'+bin(n)[2:]
    return '1'+bin(-n)[2:]

def convert_int(n: int):
    res = ''
    for c in to_bin(n):
        if c == '1':
            res += '\t'
        else:
            res += ' '
    return res

def check_labelname(labelname: str):
    return labelname != ''

labels = {}
headspaces = re.compile(r'^[ \t]*')
chars = ['\t', ' ']

def get_label(labelname: str):
    if labelname not in labels:
        labels[labelname] = 0, len(labels)
    else:
        cnt, lid = labels[labelname]
        labels[labelname] = cnt+1, lid
    return f'L{labels[labelname][1]}'

def convert_line(input_file: str, linenumber: int, line: str):
    if line == "":
        return ""
    line = headspaces.sub('', line)
    cmd = line.strip().split(' ')
    error_prefix = f'{input_file}:{linenumber}: '
    op = cmd[0]
    args = cmd[1:]
    if op == 'push':
        if len(args) != 1:
            raise RuntimeError(f'{error_prefix}command "push" takes 1 argument')
        if not is_int(args[0]):
            raise RuntimeError(f'{error_prefix}"{args[0]}" is not an integer')
        return f'  {convert_int(int(args[0]))}', '\n'
    elif op == 'printi':
        return '\t\n \t', ''
    elif op == 'printc':
        return '\t\n  ', ''
    elif op == 'dup':
        return ' \n ', ''
    elif op == 'swap':
        return ' \n\t', ''
    elif op == 'drop':
        return ' \n\n', ''
    elif op == 'add':
        return '\t   ', ''
    elif op == 'sub':
        return '\t  \t', ''
    elif op == 'mul':
        return '\t  \n', ''
    elif op == 'div':
        return '\t \t ', ''
    elif op == 'mod':
        return '\t \t\t', ''
    elif op == 'store':
        return '\t\t ', ''
    elif op == 'retrieve':
        return '\t\t\t', ''
    elif op == 'end':
        return '\n\n\n', ''
    elif op == 'readc':
        return '\t\n\t ', ''
    elif op == 'readi':
        return '\t\n\t\n', ''
    elif op == 'ret':
        return '\n\t\n', ''
    elif op == 'call':
        if len(args) != 1:
            raise RuntimeError(f'{error_prefix}command "call" takes 1 argument')
        if not check_labelname(args[0]):
            raise RuntimeError(f'{error_prefix}invalid label name: {args[0]}')
        return f'\n \t{get_label(args[0])}', '\n'
    elif op == 'jmp':
        if len(args) != 1:
            raise RuntimeError(f'{error_prefix}command "jmp" takes 1 argument')
        if not check_labelname(args[0]):
            raise RuntimeError(f'{error_prefix}invalid label name: {args[0]}')
        return f'\n \n{get_label(args[0])}', '\n'
    elif op == 'jz':
        if len(args) != 1:
            raise RuntimeError(f'{error_prefix}command "jz" takes 1 argument')
        if not check_labelname(args[0]):
            raise RuntimeError(f'{error_prefix}invalid label name: {args[0]}')
        return f'\n\t {get_label(args[0])}', '\n'
    elif op == 'jn':
        if len(args) != 1:
            raise RuntimeError(f'{error_prefix}command "jn" takes 1 argument')
        if not check_labelname(args[0]):
            raise RuntimeError(f'{error_prefix}invalid label name: {args[0]}')
        return f'\n\t\t{get_label(args[0])}', '\n'
    elif op[-1] == ':':
        labelname = op[:-1]
        return f'\n  {get_label(labelname)}', '\n'
    else:
        raise RuntimeError(f'{error_prefix}unknown command: {cmd[0]}')

def convert_labels(wscode: str):
    values = list(labels.values())
    values.sort()
    i = 0
    for _, lid in values:
        keta = 0
        total = 0
        nums = 1
        while total + nums <= i:
            keta += 1
            total += nums
            nums *= len(chars)
        rest = i - total
        labelname = f'L{lid}'
        labelcode = ""
        for j in range(keta):
            labelcode += chars[rest % len(chars)]
            rest //= len(chars)
        wscode = wscode.replace(labelname, labelcode)
        i += 1
    return wscode

def convert(input_file: str, output_file: str):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'{input_file} was not found')
    ws = ""
    nxt = ""
    reg = re.compile(r'#.*')
    with open(input_file, 'r', encoding='utf-8') as f:
        linenumber = 1
        for line in f:
            # for comments
            line = reg.sub('', line.strip())
            if line == '':
                continue
            ws += nxt
            converted, nxt = convert_line(input_file, linenumber, line)
            ws += converted
            linenumber += 1
    # convert labels
    ws = convert_labels(ws)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ws)

def main():
    args = parseargs()
    input_file = args.input
    output_file = args.output
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".ws"
    convert(input_file, output_file)

main()
