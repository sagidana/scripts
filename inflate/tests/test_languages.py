"""every code-bearing language, the same shape, through every flag

each fixture in langs/<lang>/ defines three functions in this order:

    helper            a leaf, called by nothing in the file
    greet             calls helper once
    runner            calls greet once

wrapped in a class named Box when the language has such a construct. the
names are found by scanning the fixture, so line numbers are never pinned:
`helper` must appear exactly twice (its definition, then greet's call),
`greet` exactly twice, `runner` exactly once. test_fixture_shape guards
that, so a broken fixture fails differently from a broken tool.
"""

import os
import re
import subprocess
import sys

import pytest


LANGS = os.path.join(os.path.dirname(__file__), 'langs')

HEADER = re.compile(r'^(.+?):(\d+):(\d+)(?: \((.*)\))?$')

CLASS = 'class'
PLAIN = 'plain'


# lang -> (fixture file name, whether --class has something to expand to)
FIXTURES = {}


def named(name, filename, kind=PLAIN):
    FIXTURES[name] = (filename, kind == CLASS)


named('ada', 'box.adb', CLASS)
named('al', 'Box.al', CLASS)
named('apex', 'Box.cls', CLASS)
named('arduino', 'box.ino')
named('asm', 'box.asm')
named('astro', 'box.astro')
named('awk', 'box.awk')
named('bash', 'box.sh')
named('bass', 'box.bass')
named('bicep', 'box.bicep')
named('bitbake', 'box.bb')
named('brightscript', 'box.brs')
named('c', 'box.c')
named('cairo', 'box.cairo', CLASS)
named('circom', 'box.circom')
named('clarity', 'box.clar')
named('clojure', 'box.clj')
named('cmake', 'box.cmake')
named('cobol', 'box.cob')
named('commonlisp', 'box.lisp')
named('cpp', 'box.cpp', CLASS)
named('crystal', 'box.cr', CLASS)
named('cuda', 'box.cu')
named('d', 'box.d', CLASS)
named('dart', 'box.dart', CLASS)
named('elisp', 'box.el')
named('elixir', 'box.ex', CLASS)
named('elm', 'Box.elm')
named('erlang', 'box.erl')
named('faust', 'box.dsp')
named('fennel', 'box.fnl')
named('fish', 'box.fish')
named('forth', 'box.4th')
named('fortran', 'box.f90', CLASS)
named('fsharp', 'Box.fs', CLASS)
named('func', 'box.fc')
named('gdscript', 'box.gd')
named('gleam', 'box.gleam')
named('glsl', 'box.glsl')
named('gn', 'box.gn')
named('go', 'box.go')
named('groovy', 'Box.groovy', CLASS)
named('hack', 'box.hack', CLASS)
named('hare', 'box.ha')
named('haskell', 'Box.hs')
named('haxe', 'Box.hx', CLASS)
named('hlsl', 'box.hlsl', CLASS)
named('html', 'box.html')
named('idris', 'Box.idr')
named('ispc', 'box.ispc')
named('janet', 'box.janet')
named('java', 'Box.java', CLASS)
named('javascript', 'box.js', CLASS)
named('jq', 'box.jq')
named('jsonnet', 'box.jsonnet')
named('julia', 'box.jl', CLASS)
named('kotlin', 'Box.kt', CLASS)
named('latex', 'box.tex')
named('lean', 'Box.lean', CLASS)
named('llvm', 'box.ll')
named('lua', 'box.lua')
named('luau', 'box.luau')
named('magik', 'box.magik')
named('matlab', 'box.mat', CLASS)
named('move', 'box.move', CLASS)
named('netlinx', 'box.axs')
named('nqc', 'box.nqc')
named('objc', 'box.m', CLASS)
named('ocaml', 'box.ml', CLASS)
named('odin', 'box.odin')
named('pascal', 'box.pas')
named('perl', 'box.pl', CLASS)
named('php', 'box.php', CLASS)
named('pkl', 'box.pkl')
named('pony', 'box.pony', CLASS)
named('powershell', 'box.ps1')
named('prolog', 'box.pro')
named('purescript', 'Box.purs')
named('python', 'box.py', CLASS)
named('ql', 'box.ql')
named('qmljs', 'box.qml')
named('r', 'box.r')
named('racket', 'box.rkt')
named('rego', 'box.rego')
named('rescript', 'box.res', CLASS)
named('ruby', 'box.rb', CLASS)
named('rust', 'box.rs', CLASS)
named('scala', 'Box.scala', CLASS)
named('scheme', 'box.scm')
named('scss', 'box.scss')
named('smali', 'Box.smali', CLASS)
named('solidity', 'box.sol', CLASS)
named('sql', 'box.sql')
named('squirrel', 'box.nut', CLASS)
named('starlark', 'box.bzl')
named('svelte', 'box.svelte')
named('swift', 'box.swift', CLASS)
named('tcl', 'box.tcl')
named('teal', 'box.tl')
named('templ', 'box.templ')
named('tlaplus', 'box.tla', CLASS)
named('tsx', 'box.tsx', CLASS)
named('twig', 'box.twig')
named('typescript', 'box.ts', CLASS)
named('typst', 'box.typ')
named('uxntal', 'box.tal')
named('v', 'box.v')
named('verilog', 'box.sv', CLASS)
named('vhdl', 'box.vhd', CLASS)
named('vim', 'box.vim')
named('vue', 'box.vue')
named('wast', 'box.wast', CLASS)
named('wat', 'box.wat', CLASS)
named('wgsl', 'box.wgsl')
named('wolfram', 'box.wl')
named('yuck', 'box.yuck')
named('zig', 'box.zig', CLASS)
named('zsh', 'box.zsh')

LANGUAGES = sorted(FIXTURES)


def folder_of(lang):
    return os.path.join(LANGS, lang)


def source_of(lang):
    path = os.path.join(folder_of(lang), FIXTURES[lang][0])
    with open(path, 'r', encoding='utf-8') as handle:
        return handle.read()


def rows_of(text, name):
    """1-based rows mentioning `name` as a whole word"""
    pattern = re.compile(r'(?<![A-Za-z0-9_])' + name + r'(?![A-Za-z0-9_])')
    rows = []
    row = 0
    for line in text.split('\n'):
        row = row + 1
        if pattern.search(line) is None: continue
        rows.append(row)
    return rows


class Shape:
    """where helper, greet and runner sit in one fixture"""

    def __init__(self, lang):
        text = source_of(lang)
        self.lang = lang
        self.helper = rows_of(text, 'helper')
        self.greet = rows_of(text, 'greet')
        self.runner = rows_of(text, 'runner')

    def helper_def(self):
        return self.helper[0]

    def helper_call(self):
        return self.helper[1]

    def greet_def(self):
        return self.greet[0]

    def greet_call(self):
        return self.greet[1]

    def runner_def(self):
        return self.runner[0]


def inflate(lang, row, *argv):
    """run the tool on one hit, rooted at that language's fixture folder"""
    line = '%s:%d:1:x' % (FIXTURES[lang][0], row)
    command = [sys.executable, '-m', 'inflate', '--range', '--root', '.']
    result = subprocess.run(command + list(argv),
                            cwd=folder_of(lang),
                            input=line + '\n',
                            capture_output=True,
                            text=True,
                            check=True)
    return result.stdout


def headers(output):
    """the file:start:end lines of a --range run; echoed input lines are dropped"""
    found = []
    for line in output.split('\n'):
        if not line.strip(): continue
        match = HEADER.match(line)
        if match is None: continue
        found.append((int(match.group(2)), int(match.group(3)), match.group(4)))
    return found


def covers(found, row):
    for start, end, note in found:
        if start <= row <= end: return True
    return False


@pytest.mark.parametrize('lang', LANGUAGES)
def test_fixture_shape(lang):
    """the fixture itself, before the tool is blamed for anything"""
    shape = Shape(lang)
    assert len(shape.helper) == 2, 'helper must be defined once and called once'
    assert len(shape.greet) == 2, 'greet must be defined once and called once'
    assert len(shape.runner) == 1, 'runner must be defined once and called never'
    assert shape.helper_def() < shape.greet_def() < shape.runner_def()
    assert shape.greet_def() < shape.helper_call() < shape.greet_call()


PARSE_CHECK = """
import sys
from inflate.languages import language_for, tree_for
lang, path = sys.argv[1], sys.argv[2]
found = language_for(path)
if found != lang: sys.exit('picked %s, not %s' % (found, lang))
tree = tree_for(path, lang)
if tree is None: sys.exit('no grammar')
if tree.root_node.has_error: sys.exit('grammar cannot parse the fixture')
"""


@pytest.mark.parametrize('lang', LANGUAGES)
def test_fixture_parses(lang):
    """the grammar reaches the fixture, and swallows it whole

    a fixture the grammar chokes on would fail every other test here for a
    reason that is not the tool's, so it is worth its own check. run out of
    process: a broken grammar can take the interpreter down with it.
    """
    path = os.path.join(folder_of(lang), FIXTURES[lang][0])
    result = subprocess.run([sys.executable, '-c', PARSE_CHECK, lang, path],
                            capture_output=True,
                            text=True,
                            check=False)
    assert result.returncode == 0, result.stderr.strip().split('\n')[-1]


@pytest.mark.parametrize('lang', LANGUAGES)
def test_function(lang):
    """a hit on greet's body expands to greet, and stops there"""
    shape = Shape(lang)
    found = headers(inflate(lang, shape.helper_call()))
    assert len(found) == 1, 'expected exactly one definition'
    start, end, note = found[0]
    assert start <= shape.greet_def()
    assert end >= shape.helper_call()
    assert end < shape.greet_call(), 'greet swallowed runner'


@pytest.mark.parametrize('lang', LANGUAGES)
def test_class(lang):
    """a hit inside greet expands to the whole enclosing class"""
    if not FIXTURES[lang][1]: pytest.skip('no class construct')
    shape = Shape(lang)
    found = headers(inflate(lang, shape.helper_call(), '--class'))
    assert len(found) == 1, 'expected exactly one definition'
    start, end, note = found[0]
    assert start <= shape.helper_def()
    assert end >= shape.greet_call()


@pytest.mark.parametrize('lang', LANGUAGES)
def test_class_from_its_own_declaration(lang):
    """a hit on the class's own first row expands to the same class

    the declaration line is a node of its own in some grammars (smali writes
    `.class public final Lp/x;` as a one-row class_directive inside the
    class_definition that is the whole file) and it used to win for being the
    innermost.
    """
    if not FIXTURES[lang][1]: pytest.skip('no class construct')
    shape = Shape(lang)
    inside = headers(inflate(lang, shape.helper_call(), '--class'))
    assert len(inside) == 1, 'expected exactly one definition'
    found = headers(inflate(lang, inside[0][0], '--class'))
    assert found == inside, 'the declaration row gave a different class'


@pytest.mark.parametrize('lang', LANGUAGES)
def test_callees_one(lang):
    """runner's single callee is greet"""
    shape = Shape(lang)
    found = headers(inflate(lang, shape.greet_call(), '--callees', '1'))
    assert covers(found, shape.runner_def()), 'the seed itself is missing'
    assert found[0][0] > shape.greet_def(), 'the seed widened past runner'
    assert covers(found, shape.greet_def()), 'greet was not reached from runner'


@pytest.mark.parametrize('lang', LANGUAGES)
def test_callees_two(lang):
    """two levels down from runner reaches helper"""
    shape = Shape(lang)
    found = headers(inflate(lang, shape.greet_call(), '--callees', '2'))
    assert found[0][0] > shape.greet_def(), 'the seed widened past runner'
    assert covers(found, shape.greet_def()), 'greet was not reached from runner'
    assert covers(found, shape.helper_def()), 'helper was not reached from greet'


@pytest.mark.parametrize('lang', LANGUAGES)
def test_callers_one(lang):
    """helper's single caller is greet"""
    shape = Shape(lang)
    found = headers(inflate(lang, shape.helper_def(), '--callers', '1'))
    assert covers(found, shape.helper_def()), 'the seed itself is missing'
    assert found[0][1] < shape.greet_def(), 'the seed widened past helper'
    assert covers(found, shape.greet_def()), 'greet was not found as a caller'


@pytest.mark.parametrize('lang', LANGUAGES)
def test_callers_two(lang):
    """two levels up from helper reaches runner"""
    shape = Shape(lang)
    found = headers(inflate(lang, shape.helper_def(), '--callers', '2'))
    assert found[0][1] < shape.greet_def(), 'the seed widened past helper'
    assert covers(found, shape.greet_def()), 'greet was not found as a caller'
    assert covers(found, shape.runner_def()), 'runner was not found as a caller'
