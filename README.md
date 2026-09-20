# shell utilities

small command line tools in the spirit of the unix text utilities: each reads
lines on stdin, writes lines on stdout, warns on stderr, and composes with
`rg`, `sort`, `xargs`, `fzf` and each other.

one directory per utility, each a standalone pip-installable package with
its own README, tests and console script:

    pip install ./enclose
    pip install ./each

or all of them at once, extra arguments going to pip (`--user`, `-e`, ...):

    ./install.sh
    ./install.sh --user

`install.sh` also links every tool's bash completion into
`~/.local/share/bash-completion/completions/`, where the bash-completion
package loads it on first use in a new shell. without bash-completion, one
line in `.bashrc` does the same:

    source /path/to/repo/completion.bash

| utility | job |
| --- | --- |
| [enclose](enclose/) | print the whole function or class that `rg --vimgrep` hits sit in |
| [each](each/) | run a command pipeline once per input line, the line on its stdin |

## examples

the snippets below run in `enclose/tests/fixtures`, so the output shown is real.

### enclose

`rg --vimgrep` gives `file:line:col:text` hits; `enclose` turns every hit into
the function it sits in, printed once as a `file:start:end` header followed
by the function's lines. hits outside any function are echoed unchanged:

    $ rg --vimgrep 'helper\(' sample.py | enclose
    sample.py:4:5
    def helper(value):
        return value + 1

    sample.py:14:16
        def grow(self):
            self.size = helper(self.size)
            return self.size

    sample.py:25:29
    def use_widget():
        widget = Widget(3)
        callback = lambda x: helper(x)
        widget.grow()
        return callback(widget.size)

    sample.py:32:13:TOP_LEVEL = helper(41)

`--range` keeps only the headers, so the answer to "which functions mention
this" is one line per function:

    $ rg --vimgrep 'helper\(' sample.py | enclose --range
    sample.py:4:5
    sample.py:14:16
    sample.py:25:29
    sample.py:32:13:TOP_LEVEL = helper(41)

`--class` widens to the enclosing class, struct, impl or module instead:

    $ rg --vimgrep 'self.size = helper' sample.py | enclose --class --range
    sample.py:8:22

`--callers N` adds the functions that call the result, `N` levels deep; every
extra block says why it is there. `--callees N` goes the other way. both look
through every file of the same language under `--root` (default: cwd):

    $ rg --vimgrep 'def helper' sample.py | enclose --callers 1 --range
    sample.py:4:5
    sample.py:14:16 (caller of helper, depth 1)
    sample.py:25:29 (caller of helper, depth 1)
    sample.py:27:27 (caller of helper, depth 1)

    $ rg --vimgrep 'int main' sample.c | enclose --callees 2 --range
    sample.c:18:23
    sample.c:12:16 (callee of main, depth 1)
    sample.c:7:10 (callee of grow, depth 2)

by default the innermost *named* function wins, so a hit inside a lambda or
callback expands to the function holding it. `--inner` takes the anonymous
one, `--outer` the outermost:

    $ rg --vimgrep 'lambda' sample.py | enclose --inner
    sample.py:27:27
        callback = lambda x: helper(x)

    $ rg --vimgrep 'return n - 1' sample.py | enclose --outer --range
    sample.py:18:22

hits can also be arguments, or files holding hits, and `file:line:text` (from
`rg -Hn`) works as well as `file:line:col:text`:

    $ enclose --range sample.go:14:11 sample.rs:11:21
    sample.go:13:16
    sample.rs:10:13

    $ rg -Hn 'def helper' sample.py | enclose --range
    sample.py:4:5

    $ rg --vimgrep 'helper\(' sample.py > hits && enclose --range hits

the grammar comes from the extension, well-known file names, or the shebang
of extensionless scripts; `--lang` overrides it for every file:

    $ rg --vimgrep 'helper' run | enclose --range
    run:3:4
    run:7:7:print(helper(1))

    $ rg --vimgrep 'helper' weird.ext | enclose --lang python

`enclose`'s output is valid input again, so it chains with itself and with
anything that reads `file:line`:

    rg --vimgrep todo | enclose --range | sort -u | wc -l
    rg --vimgrep todo | enclose --range | enclose --callers 1
    rg --vimgrep todo | enclose --range | fzf | cut -d: -f1,2 | xargs -I{} vim +{}
    rg --vimgrep todo | enclose | less

### each

`each` runs a command once per input line, the line on the command's stdin,
and prints every run as a block: the line, the output, a blank line:

    $ printf 'abc\nxyz\n' | each tr a-z A-Z
    abc
    ABC

    xyz
    XYZ

the command is typed unquoted, so the shell completes it as usual. stages of
a pipeline are separated by `\|`, the pipe escaped so the shell leaves it to
`each`. no shell runs the stages: the words reach the commands exactly as
typed, with no second round of quoting or globbing:

    $ seq 3 | each tr a-z A-Z \| rev
    1
    1

    2
    2

    3
    3

`-j N` runs `N` lines at a time. blocks still come out in input order:

    $ seq 3 | each -j3 sh -c 'sleep 0.$(( 4 - $(cat) )); echo done'
    1
    done

    2
    done

    3
    done

the line is on stdin, not in the arguments. when a command wants it as an
argument, a one-line `sh -c` bridges the two:

    $ ls sample.py sample.c | each sh -c 'read file; wc -l "$file"'
    sample.c
    23 sample.c

    sample.py
    32 sample.py

exit status is 1 when any run failed (any stage exited non-zero), so `each`
works as a guard in scripts:

    $ seq 2 | each sh -c 'read n; test "$n" != 2'; echo "rc=$?"
    1

    2

    rc=1

### together

`enclose` reads all hits at once and answers per function; `each` makes any
other line-at-a-time tool do the same. the shapes compose:

    # ask a model about every function that mentions a todo, four at a time
    rg --vimgrep todo | each -j4 enclose \| cai -- is this urgent?

    # one block per hit: the hit, then every caller of its function
    rg --vimgrep todo | enclose --range | each enclose --callers 1 --range

    # line count of every function that mentions a todo
    rg --vimgrep todo | each enclose \| wc -l

## conventions

- input and output lines are `file:line:col:text` (rg's `--vimgrep` shape)
  or the shorter `file:start:end`; a tool's own output is valid input again
- lines a tool cannot handle are echoed unchanged, never dropped
- one job per tool, flags only for how that job is done
- no `#` comments; one guard per line; dicts and sets built line by line
