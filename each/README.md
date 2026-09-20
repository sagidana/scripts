# each

run a command pipeline once per input line, the line on its stdin.

    rg --vimgrep todo | each -j4 enclose \| cai -- is this urgent?
    seq 3 | each tr a-z A-Z \| rev

the words after each's own flags are the command, typed unquoted so the
shell completes them as usual. a literal `|` word (escaped from the shell as
`\|`) separates pipeline stages. no shell is involved in running them: the
words are passed to the commands exactly as typed, so there is no second
round of quoting or globbing. redirections and `&&` are not supported; each
builds pipes, nothing more.

every input line is fed to the first stage's stdin and the last stage's
stdout is printed as one block: the line itself, then the output, then a
blank line. blocks come out in input order even when jobs run in parallel.
blank input lines are skipped. stderr of the commands passes through.

    -j N, --jobs N    run N lines at a time (default 1)

exit status is 1 when any job failed (any stage exited non-zero), else 0.

    $ seq 3 | each -j2 tr a-z A-Z \| rev
    1
    1

    2
    2

    3
    3

## install

    pip install .

## completion

register `each` the way `sudo` and `xargs` are registered, so the shell
completes the command after it:

    complete -F _command each                             # bash
    complete -c each -x -a '(__fish_complete_subcommand)'  # fish

## test

    pip install .[test]
    pytest
