import os
import subprocess
import sys

import pytest

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


def inflate(*argv, stdin=''):
    result = subprocess.run([sys.executable, '-m', 'inflate'] + list(argv),
                            cwd=FIXTURES,
                            input=stdin,
                            capture_output=True,
                            text=True,
                            check=True)
    return result.stdout


def test_hit_expands_to_enclosing_function():
    out = inflate(stdin='sample.py:15:21:        self.size = helper(self.size)\n')
    assert out == 'sample.py:14:16\n    def grow(self):\n        self.size = helper(self.size)\n        return self.size\n\n'


def test_hit_outside_any_function_is_echoed():
    out = inflate(stdin='sample.py:32:13:TOP_LEVEL = helper(41)\n')
    assert out == 'sample.py:32:13:TOP_LEVEL = helper(41)\n'


def test_unknown_language_is_echoed():
    out = inflate(stdin='notes.txt:1:1:helper is mentioned here too\n')
    assert out == 'notes.txt:1:1:helper is mentioned here too\n'


def test_same_function_printed_once():
    hits = 'sample.py:15:21:x\nsample.py:16:16:y\n'
    assert inflate('--range', stdin=hits) == 'sample.py:14:16\n'


def test_range_prints_only_headers():
    hits = 'sample.py:15:21:x\nsample.py:32:13:TOP_LEVEL = helper(41)\n'
    assert inflate('--range', stdin=hits) == 'sample.py:14:16\nsample.py:32:13:TOP_LEVEL = helper(41)\n'


def test_range_output_is_accepted_as_input():
    assert inflate('--range', stdin='sample.py:14:16\n') == 'sample.py:14:16\n'


def test_line_without_column():
    assert inflate('--range', stdin='sample.py:15:some text\n') == 'sample.py:14:16\n'


def test_class():
    assert inflate('--class', '--range', stdin='sample.py:15:21:x\n') == 'sample.py:8:22\n'


def test_inner_includes_lambda():
    hit = 'sample.py:27:26:    callback = lambda x: helper(x)\n'
    assert inflate('--range', stdin=hit) == 'sample.py:25:29\n'
    assert inflate('--range', '--inner', stdin=hit) == 'sample.py:27:27\n'


def test_outer_picks_outermost():
    hit = 'sample.py:21:20:            return n - 1\n'
    assert inflate('--range', stdin=hit) == 'sample.py:20:21\n'
    assert inflate('--range', '--outer', stdin=hit) == 'sample.py:18:22\n'


def test_callers():
    out = inflate('--range', '--callers', '1', stdin='sample.py:4:5:def helper(value):\n')
    assert out == ('sample.py:4:5\n'
                   'sample.py:14:16 (caller of helper, depth 1)\n'
                   'sample.py:25:29 (caller of helper, depth 1)\n'
                   'sample.py:27:27 (caller of helper, depth 1)\n')


def test_callees():
    out = inflate('--range', '--callees', '2', stdin='sample.c:19:1:x\n')
    assert out == ('sample.c:18:23\n'
                   'sample.c:12:16 (callee of main, depth 1)\n'
                   'sample.c:7:10 (callee of grow, depth 2)\n')


def test_root_limits_the_index(tmp_path):
    out = inflate('--range', '--callers', '1', '--root', str(tmp_path), stdin='sample.py:4:5:x\n')
    assert out == 'sample.py:4:5\n'


def test_lines_as_arguments_and_dash_for_stdin():
    out = inflate('--range', 'sample.go:14:11:x', '-', stdin='sample.rs:11:21:x\n')
    assert out == 'sample.go:13:16\nsample.rs:10:13\n'


def test_file_of_hits_as_argument(tmp_path):
    hits = tmp_path / 'hits'
    hits.write_text('sample.el:6:3:x\n')
    assert inflate('--range', str(hits)) == 'sample.el:5:6\n'


def test_shebang_picks_the_grammar():
    assert inflate('--range', stdin='run:4:5:x\n') == 'run:3:4\n'


def test_lang_forces_the_grammar():
    assert inflate('--range', '--lang', 'python', stdin='notes.txt:1:1:x\n') == 'notes.txt:1:1:x\n'


def test_script_inside_html():
    assert inflate('--range', stdin='sample.html:9:10:x\n') == 'sample.html:8:10\n'


def test_blank_lines_are_dropped():
    assert inflate('--range', stdin='\n\nsample.py:15:21:x\n\n') == 'sample.py:14:16\n'


def test_hit_on_leading_whitespace_expands_to_the_def_on_that_line():
    hits = 'sample.py:14:1:    def grow(self):\nsample.py:20:1:        def inner(n):\n'
    assert inflate('--range', stdin=hits) == 'sample.py:14:16\nsample.py:20:21\n'
