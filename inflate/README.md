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
a hit with no enclosing function falls back to the enclosing class, which is
the only answer there is in a language whose file is one class -- every hit
on a smali directive or field. a file's own root does not count, so a stray
top-level line is not dragged out to the whole module. hits outside both, or
in files without a grammar, are echoed unchanged, so nothing is lost in a
pipeline.

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

`tests/test_inflate.py` covers the pipeline itself. `tests/test_languages.py`
covers the grammars: `tests/langs/<lang>/` holds one small fixture per
code-bearing language, all written to the same shape --

    helper      a leaf
    greet       calls helper
    runner      calls greet

inside a class named `Box` where the language has one. every fixture is run
through `--function`, `--class`, `--callees 1`, `--callees 2`, `--callers 1`
and `--callers 2`. line numbers are never pinned: the three names are found
by scanning the fixture, so a fixture stays editable. two guards keep a bad
fixture from reading as a bad tool -- `test_fixture_shape` checks the name
layout, `test_fixture_parses` checks the grammar swallows the file whole.

a language failing there is a real gap in `nodes.py`'s classification (or in
the grammar itself), not a flaky test.
