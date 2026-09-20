# inflate

print the whole function (or class) that `rg --vimgrep` hits sit in.

    rg --vimgrep pattern | inflate
    rg --vimgrep pattern | inflate --class
    rg --vimgrep pattern | inflate --callees 2 --callers 1

each input line is `file:line:col:text` (also `file:line:text` and
`file:line:col`), read from stdin, from files named as arguments, or given
directly as arguments (so `xargs -n 1 inflate` works). the file is parsed with
tree-sitter (grammar picked from the file name or shebang, fetched by
tree-sitter-language-pack on first use) and the innermost named function
enclosing the hit is printed once as `file:start:end` followed by its lines.
hits outside any function, or in files without a grammar, are echoed
unchanged, so nothing is lost in a pipeline.

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
language under `--root`, so overloads and same-named methods all show up.

## install

    pip install .

needs `rg` on PATH for `--callers`/`--callees` (falls back to walking the
tree without it).

## composing

`--range` is the machine-readable half: one `file:start:end` line per
definition, no bodies. those lines are valid input again, so the tool chains
with itself and with anything that understands `file:line`:

    rg --vimgrep todo | inflate --range | sort -u
    rg --vimgrep todo | inflate --range | inflate --callers 1
    rg --vimgrep todo | inflate --range | fzf | cut -d: -f1,2 | xargs -I{} vim +{}
    rg --vimgrep todo | inflate | less

## test

    pip install .[test]
    pytest
