"""print the whole function (or class) that `rg --vimgrep` hits sit in.

    rg --vimgrep pattern | inflate
    rg --vimgrep pattern | inflate --class
    rg --vimgrep pattern | inflate --callees 2 --callers 1

each input line is `file:line:col:text` (also `file:line:text`), read from
stdin, from files named as arguments, or given directly as arguments (so
`xargs -n 1 inflate` works). the file is parsed with tree-sitter (grammar
picked from the file name or shebang, fetched by tree-sitter-language-pack on
first use) and the innermost named function enclosing the hit is printed once
as `file:start:end` followed by its lines. hits outside any function, or in
files without a grammar, are echoed unchanged.

    --function    expand to the enclosing function (default)
    --class       expand to the enclosing class/struct/module instead
    --callees N   also expand functions called from the result, N levels deep
    --callers N   also expand functions that call the result, N levels deep
    --root DIR    where callers/callees are looked for (default: cwd)
    --range       print only `file:start:end` lines
    --inner       innermost function, anonymous ones included
    --outer       outermost enclosing function
    --lang X      force grammar X for every file

callers and callees are matched by name across every file of the same
language under --root, so overloads and same-named methods all show up.
"""

import argparse
import os
import signal
import sys

import inflate
from inflate.targets import expand_line, index_for


def emit(target, note, args):
    header = target.header()
    if note: header = header + ' ' + note
    print(header)
    if args.range: return
    print(target.lines())
    print()


def walk_related(seeds, depth, relation, seen, args):
    """breadth-first over callees or callers, `depth` levels from the seeds"""
    frontier = seeds
    level = 0
    while frontier and level < depth:
        level = level + 1
        following = []
        for target in frontier:
            index = index_for(target.lang, args.root)
            related = []
            if relation == 'callee': related = index.callees_of(target)
            if relation == 'caller': related = index.callers_of(target)
            for other in related:
                if other.key() in seen: continue
                seen.add(other.key())
                note = '(%s of %s, depth %d)' % (relation, target.name, level)
                emit(other, note, args)
                following.append(other)
        frontier = following


def read_inputs(inputs):
    """every input line: stdin when no inputs (or `-`), file contents, or the argument itself"""
    lines = []
    if not inputs:
        lines = sys.stdin.read().splitlines()
    for item in inputs:
        if item == '-':
            lines.extend(sys.stdin.read().splitlines())
            continue
        if os.path.isfile(item):
            with open(item, 'r', encoding='utf-8', errors='replace') as handle:
                lines.extend(handle.read().splitlines())
            continue
        lines.append(item)
    return lines


def parse_args(argv):
    argparser = argparse.ArgumentParser(prog='inflate',
                                        description=__doc__.split('\n\n')[0])
    argparser.add_argument('inputs',
                           nargs='*',
                           metavar='FILE_OR_LINE',
                           help='rg --vimgrep lines, or files holding them (default stdin, also -)')
    argparser.add_argument('--function',
                           action='store_true',
                           help='expand to the enclosing function (default)')
    argparser.add_argument('--class',
                           dest='klass',
                           action='store_true',
                           help='expand to the enclosing class/struct/module')
    argparser.add_argument('--callees',
                           type=int,
                           default=0,
                           metavar='N',
                           help='also expand called functions, N levels deep')
    argparser.add_argument('--callers',
                           type=int,
                           default=0,
                           metavar='N',
                           help='also expand calling functions, N levels deep')
    argparser.add_argument('--root',
                           default='.',
                           help='project root searched for callers/callees')
    argparser.add_argument('--range',
                           action='store_true',
                           help='print only file:start:end lines')
    argparser.add_argument('--inner',
                           action='store_true',
                           help='innermost function, anonymous ones included')
    argparser.add_argument('--outer',
                           action='store_true',
                           help='outermost enclosing function')
    argparser.add_argument('--lang',
                           default=None,
                           help='force this tree-sitter grammar for every file')
    argparser.add_argument('--version',
                           action='version',
                           version='inflate ' + inflate.__version__)
    args = argparser.parse_args(argv)
    args.mode = 'named'
    if args.inner: args.mode = 'inner'
    if args.outer: args.mode = 'outer'
    args.kind = 'function'
    if args.klass: args.kind = 'class'
    return args


def run(args):
    seen = set()
    seeds = []
    for line in read_inputs(args.inputs):
        if not line.strip(): continue
        target = expand_line(line, args)
        if target is None:
            print(line)
            continue
        if target.key() in seen: continue
        seen.add(target.key())
        seeds.append(target)
        emit(target, '', args)
    walk_related(seeds, args.callees, 'callee', seen, args)
    walk_related(seeds, args.callers, 'caller', seen, args)


def main(argv=None):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    run(parse_args(argv))


if __name__ == '__main__':
    main()
