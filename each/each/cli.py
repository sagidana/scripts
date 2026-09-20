"""run a command pipeline once per input line, the line on its stdin.

    rg --vimgrep todo | each -j4 inflate \| cai -- is this urgent?
    seq 3 | each tr a-z A-Z \| rev

the words after each's own flags are the command; a literal `|` word (escaped
from the shell as `\|`) separates pipeline stages. no shell is involved: the
words are passed to the commands exactly as typed. every input line is fed to
the first stage's stdin and the last stage's stdout is printed as one block:
the line itself, then the output, then a blank line. blocks come out in input
order even when jobs run in parallel, and a job's stderr is printed on
each's stderr together with its block, so parallel jobs never interleave.
blank input lines are skipped.

    -j N, --jobs N    run N lines at a time (default 1)

exit status is 1 when any job failed (any stage exited non-zero), else 0.
"""

import argparse
import concurrent.futures
import os
import subprocess
import sys
import threading

import each


def stages_of(words):
    """the command as a list of argv lists, split on the literal `|` word, or None"""
    stages = []
    stage = []
    for word in words:
        if word != '|':
            stage.append(word)
            continue
        stages.append(stage)
        stage = []
    stages.append(stage)
    for stage in stages:
        if not stage: return None
    return stages


def drain(handle, chunks):
    chunks.append(handle.read())
    handle.close()


def run_job(stages, line):
    """(status, output, errors) of the pipeline fed one line; status is the first non-zero exit"""
    processes = []
    errors_read, errors_write = os.pipe()
    try:
        for stage in stages:
            stdin = subprocess.PIPE
            if processes: stdin = processes[-1].stdout
            process = subprocess.Popen(stage, stdin=stdin, stdout=subprocess.PIPE, stderr=errors_write)
            processes.append(process)
    except OSError as error:
        os.close(errors_write)
        os.close(errors_read)
        for process in processes:
            process.kill()
        sys.stderr.write('each: %s: %s\n' % (stage[0], error.strerror))
        return 127, '', ''
    os.close(errors_write)
    for process in processes[:-1]:
        process.stdout.close()
    chunks = []
    reader = threading.Thread(target=drain, args=(os.fdopen(errors_read, 'rb'), chunks))
    reader.start()
    first = processes[0]
    last = processes[-1]
    try:
        first.stdin.write(line.encode('utf-8') + b'\n')
        first.stdin.close()
    except BrokenPipeError:
        pass
    output = last.stdout.read().decode('utf-8', 'replace')
    status = 0
    for process in processes:
        code = process.wait()
        if status == 0: status = code
    reader.join()
    errors = chunks[0].decode('utf-8', 'replace')
    return status, output, errors


def emit(line, output, errors):
    """one block on stdout, and the job's stderr on stderr, at the same moment"""
    sys.stdout.write(line + '\n')
    if output: sys.stdout.write(output)
    if output and not output.endswith('\n'): sys.stdout.write('\n')
    sys.stdout.write('\n')
    sys.stdout.flush()
    if not errors: return
    sys.stderr.write(errors)
    if not errors.endswith('\n'): sys.stderr.write('\n')
    sys.stderr.flush()


def parse_args(argv):
    argparser = argparse.ArgumentParser(prog='each',
                                        description=__doc__.split('\n\n')[0],
                                        usage='each [-j N] COMMAND [ARG ...] [\\| COMMAND [ARG ...]] ...')
    argparser.add_argument('-j',
                           '--jobs',
                           type=int,
                           default=1,
                           metavar='N',
                           help='run N lines at a time (default 1)')
    argparser.add_argument('--version',
                           action='version',
                           version='each ' + each.__version__)
    argparser.add_argument('command',
                           nargs=argparse.REMAINDER,
                           metavar='COMMAND',
                           help='the pipeline to run per line, stages separated by a `|` word')
    args = argparser.parse_args(argv)
    if args.jobs < 1: argparser.error('--jobs must be at least 1')
    return args


def run(args):
    stages = stages_of(args.command)
    if stages is None:
        sys.stderr.write('each: expected a command, with `|` between pipeline stages\n')
        return 2
    failed = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        lines = []
        futures = []
        for line in sys.stdin:
            line = line.rstrip('\n')
            if not line.strip(): continue
            lines.append(line)
            futures.append(pool.submit(run_job, stages, line))
        for line, future in zip(lines, futures):
            status, output, errors = future.result()
            if status != 0: failed = True
            emit(line, output, errors)
    if failed: return 1
    return 0


def main(argv=None):
    try:
        return run(parse_args(argv))
    except BrokenPipeError:
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return 141


if __name__ == '__main__':
    sys.exit(main())
