"""targets: the definition around one rg hit, and the per-language index of callers/callees"""

import os
import re
import subprocess

from inflate.languages import (language_for,
                              lines_for,
                              parser_for,
                              source_for,
                              tree_for,
                              warn)
from inflate.nodes import (calls_in,
                          descendants,
                          embedded_script,
                          find_definition,
                          climb_wrappers,
                          is_anonymous_node,
                          is_class_node,
                          is_function_node,
                          is_inner_duplicate,
                          is_nested_fragment,
                          leaf_at,
                          mentions_in,
                          name_of,
                          rows_of,
                          widen)


SKIP_DIRS = set()
SKIP_DIRS.add('.git')
SKIP_DIRS.add('.hg')
SKIP_DIRS.add('.svn')
SKIP_DIRS.add('node_modules')
SKIP_DIRS.add('__pycache__')
SKIP_DIRS.add('.venv')
SKIP_DIRS.add('venv')
SKIP_DIRS.add('build')
SKIP_DIRS.add('dist')
SKIP_DIRS.add('target')
SKIP_DIRS.add('.tox')
SKIP_DIRS.add('.mypy_cache')
SKIP_DIRS.add('.pytest_cache')

VIMGREP_LINE = re.compile(r'^(.+?):(\d+)(?::(\d+))?(?::(.*))?$')


class Target:
    """one thing to print: a node in a parsed file"""

    def __init__(self, path, lang, source, node):
        self.path = path
        self.lang = lang
        self.source = source
        self.node = node
        self.start_row, self.end_row = rows_of(node)
        # a grammar can hand back the body alone, with the signature beside it
        # rather than above it; the name is written in the signature
        self.name = name_of(widen(node)[0], self.source)

    def key(self):
        return (os.path.abspath(self.path), self.start_row, self.end_row)

    def header(self):
        return '%s:%d:%d' % (self.path, self.start_row + 1, self.end_row + 1)

    def lines(self):
        rows = lines_for(self.path)
        chunk = b'\n'.join(rows[self.start_row:self.end_row + 1])
        return chunk.decode('utf-8', 'replace')

    def scan_nodes(self):
        """the nodes this definition's calls can be written in

        a grammar that splits a definition into a signature and a body indexes
        the signature, and the calls are all in the body next to it.
        """
        start, end = widen(self.node)
        if start == end: return [self.node]
        return [start, end]

    def defined_names(self):
        """own name plus the names of functions defined inside (class members)"""
        names = set()
        if self.name: names.add(self.name)
        for child in descendants(self.node):
            if child == self.node: continue
            if not is_function_node(child, self.source): continue
            if is_anonymous_node(child, self.source): continue
            name = name_of(child, self.source)
            if name: names.add(name)
        return names



def embedded_target(path, lang, source, host, row, col, args):
    parser = parser_for('typescript')
    if parser is None: return None
    inner_source = source[host.start_byte:host.end_byte]
    inner_root = parser.parse(inner_source).root_node
    inner_row = row - host.start_point.row
    inner_col = col
    if inner_row == 0: inner_col = col - host.start_point.column
    node = find_definition(inner_root, inner_source, inner_row, inner_col, args)
    if node is None: return None
    target = Target(path, 'typescript', inner_source, node)
    target.start_row = target.start_row + host.start_point.row
    target.end_row = target.end_row + host.start_point.row
    target.source = source
    return target


def expand_line(line, args):
    """the Target for one rg line, or None when it cannot be expanded"""
    match = VIMGREP_LINE.match(line)
    if match is None: return None
    path = match.group(1)
    row = int(match.group(2)) - 1
    col = 0
    if match.group(3) is not None: col = int(match.group(3)) - 1
    source = source_for(path)
    if source is None: return None
    lang = args.lang
    if lang is None: lang = language_for(path)
    if lang is None:
        warn('ext:' + path, 'inflate: unknown language for %s' % path)
        return None
    tree = tree_for(path, lang)
    if tree is None: return None
    lines = lines_for(path)
    if row >= len(lines): return None
    text = lines[row]
    if col >= len(text): col = len(text) - 1
    if col < 0: col = 0
    while col < len(text) - 1 and text[col] in b' \t': col = col + 1
    leaf = leaf_at(tree.root_node, row, col)
    if leaf is None: return None
    host = embedded_script(leaf)
    if host is not None: return embedded_target(path, lang, source, host, row, col, args)
    node = find_definition(tree.root_node, source, row, col, args)
    if node is None: return None
    return Target(path, lang, source, node)


def project_files(root):
    listed = None
    try:
        result = subprocess.run(['rg', '--files'],
                                cwd=root,
                                stdin=subprocess.DEVNULL,
                                capture_output=True,
                                text=True,
                                check=False)
        if result.returncode in (0, 1): listed = result.stdout.splitlines()
    except OSError:
        listed = None
    if listed is None:
        listed = []
        for folder, dirs, files in os.walk(root):
            kept = []
            for name in dirs:
                if name in SKIP_DIRS: continue
                kept.append(name)
            dirs[:] = kept
            for name in files:
                listed.append(os.path.relpath(os.path.join(folder, name), root))
    paths = []
    for name in listed:
        if root == '.':
            paths.append(name)
            continue
        paths.append(os.path.join(root, name))
    return paths


def inside(inner, outer):
    if os.path.abspath(inner.path) != os.path.abspath(outer.path): return False
    if inner.node.start_byte < outer.node.start_byte: return False
    return inner.node.end_byte <= outer.node.end_byte


class Index:
    """every named function and class of one language under root"""

    def __init__(self, lang, root):
        self.lang = lang
        self.root = root
        self.functions = []
        self.classes = []
        self.by_name = {}
        self.callees = {}
        self.calls = {}
        self.build()

    def add(self, target):
        if target.name is None: return
        self.by_name.setdefault(target.name, []).append(target)

    def build(self):
        for path in project_files(self.root):
            if language_for(path) != self.lang: continue
            source = source_for(path)
            if source is None: continue
            tree = tree_for(path, self.lang)
            if tree is None: continue
            for node in descendants(tree.root_node):
                if is_class_node(node, source):
                    self.classes.append(Target(path, self.lang, source, node))
                    continue
                if not is_function_node(node, source): continue
                if is_inner_duplicate(node, source): continue
                if is_nested_fragment(node, source): continue
                if not is_anonymous_node(node, source):
                    target = Target(path, self.lang, source, node)
                    self.functions.append(target)
                    self.add(target)
                    continue
                wrapper = climb_wrappers(node)
                if wrapper == node: continue
                target = Target(path, self.lang, source, wrapper)
                self.functions.append(target)
                self.add(target)

    def knows_any(self, names):
        for name in names:
            if name in self.by_name: return True
        return False

    def calls_from(self, target):
        """the names one function calls

        by call node where the grammar labels one, else by the names it
        mentions. roughly a quarter of grammars never label a call, and a few
        more label it but hand back the wrong word, so a call node that names
        nothing in the index counts as nothing found.
        """
        key = target.key()
        if key in self.calls: return self.calls[key]
        found = set()
        for node in target.scan_nodes():
            found.update(calls_in(node, target.source))
        if not self.knows_any(found):
            for node in target.scan_nodes():
                found.update(mentions_in(node, target.source, self.by_name, target.name))
        self.calls[key] = found
        return found

    def callees_of(self, target):
        key = target.key()
        if key in self.callees: return self.callees[key]
        found = []
        for name in sorted(self.calls_from(target)):
            for callee in self.by_name.get(name, []):
                found.append(callee)
        self.callees[key] = found
        return found

    def callers_of(self, target):
        wanted = target.defined_names()
        if not wanted: return []
        found = []
        for function in self.functions:
            if function.key() == target.key(): continue
            if inside(function, target): continue
            if not self.calls_from(function) & wanted: continue
            found.append(function)
        return found


_indexes = {}


def index_for(lang, root):
    key = (lang, root)
    if key in _indexes: return _indexes[key]
    _indexes[key] = Index(lang, root)
    return _indexes[key]

