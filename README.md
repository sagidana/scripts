# shell utilities

small command line tools in the spirit of the unix text utilities: each reads
lines on stdin, writes lines on stdout, warns on stderr, and composes with
`rg`, `sort`, `xargs`, `fzf` and each other.

one directory per utility, each a standalone pip-installable package with
its own README, tests and console script:

    pip install ./enclose

| utility | job |
| --- | --- |
| [enclose](enclose/) | print the whole function or class that `rg --vimgrep` hits sit in |

## conventions

- input and output lines are `file:line:col:text` (rg's `--vimgrep` shape)
  or the shorter `file:start:end`; a tool's own output is valid input again
- lines a tool cannot handle are echoed unchanged, never dropped
- one job per tool, flags only for how that job is done
- no `#` comments; one guard per line; dicts and sets built line by line
