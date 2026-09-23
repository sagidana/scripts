"""tree-sitter node classification: functions, classes, calls, names, by node type tokens"""

import re


FUNCTION_TOKENS = set()
FUNCTION_TOKENS.add('function')
FUNCTION_TOKENS.add('method')
FUNCTION_TOKENS.add('func')
FUNCTION_TOKENS.add('fn')
FUNCTION_TOKENS.add('fun')
FUNCTION_TOKENS.add('proc')
FUNCTION_TOKENS.add('procedure')
FUNCTION_TOKENS.add('subroutine')
FUNCTION_TOKENS.add('subprogram')
FUNCTION_TOKENS.add('sub')
FUNCTION_TOKENS.add('constructor')
FUNCTION_TOKENS.add('destructor')
FUNCTION_TOKENS.add('lambda')
FUNCTION_TOKENS.add('closure')
FUNCTION_TOKENS.add('defun')
FUNCTION_TOKENS.add('defn')
FUNCTION_TOKENS.add('def')
FUNCTION_TOKENS.add('defs')
FUNCTION_TOKENS.add('funcdef')
FUNCTION_TOKENS.add('task')
FUNCTION_TOKENS.add('predicate')
FUNCTION_TOKENS.add('macro')

NOT_FUNCTION_TOKENS = set()
NOT_FUNCTION_TOKENS.add('call')
NOT_FUNCTION_TOKENS.add('calls')
NOT_FUNCTION_TOKENS.add('invocation')
NOT_FUNCTION_TOKENS.add('application')
NOT_FUNCTION_TOKENS.add('type')
NOT_FUNCTION_TOKENS.add('types')
NOT_FUNCTION_TOKENS.add('pointer')
NOT_FUNCTION_TOKENS.add('parameter')
NOT_FUNCTION_TOKENS.add('parameters')
NOT_FUNCTION_TOKENS.add('param')
NOT_FUNCTION_TOKENS.add('params')
NOT_FUNCTION_TOKENS.add('argument')
NOT_FUNCTION_TOKENS.add('arguments')
NOT_FUNCTION_TOKENS.add('name')
NOT_FUNCTION_TOKENS.add('identifier')
NOT_FUNCTION_TOKENS.add('declarator')
NOT_FUNCTION_TOKENS.add('modifier')
NOT_FUNCTION_TOKENS.add('modifiers')
NOT_FUNCTION_TOKENS.add('reference')
NOT_FUNCTION_TOKENS.add('keyword')
NOT_FUNCTION_TOKENS.add('clause')
NOT_FUNCTION_TOKENS.add('attribute')
NOT_FUNCTION_TOKENS.add('annotation')
NOT_FUNCTION_TOKENS.add('import')
NOT_FUNCTION_TOKENS.add('export')
NOT_FUNCTION_TOKENS.add('prototype')
NOT_FUNCTION_TOKENS.add('proto')
NOT_FUNCTION_TOKENS.add('head')
NOT_FUNCTION_TOKENS.add('header')
NOT_FUNCTION_TOKENS.add('left')
NOT_FUNCTION_TOKENS.add('spec')

FUNCTION_EXACT = set()
FUNCTION_EXACT.add('clause_term')
FUNCTION_EXACT.add('word_definition')
FUNCTION_EXACT.add('operator_definition')
FUNCTION_EXACT.add('mixin_statement')
FUNCTION_EXACT.add('new_command_definition')
FUNCTION_EXACT.add('bind')
FUNCTION_EXACT.add('rule')

INNER_BODY_TYPES = set()
INNER_BODY_TYPES.add('function_body')
INNER_BODY_TYPES.add('method_body')
INNER_BODY_TYPES.add('constructor_body')
INNER_BODY_TYPES.add('procedure_body')
INNER_BODY_TYPES.add('lambda_body')
INNER_BODY_TYPES.add('func_body')
INNER_BODY_TYPES.add('fun_body')

BODY_TOKENS = set()
BODY_TOKENS.add('body')
BODY_TOKENS.add('block')
BODY_TOKENS.add('statements')
BODY_TOKENS.add('suite')
BODY_TOKENS.add('sequence')

ANONYMOUS_TOKENS = set()
ANONYMOUS_TOKENS.add('lambda')
ANONYMOUS_TOKENS.add('closure')
ANONYMOUS_TOKENS.add('arrow')
ANONYMOUS_TOKENS.add('literal')
ANONYMOUS_TOKENS.add('anonymous')
ANONYMOUS_TOKENS.add('expression')

HEADER_CHILD_TYPES = set()
HEADER_CHILD_TYPES.add('FnProto')

CLASS_TOKENS = set()
CLASS_TOKENS.add('class')
CLASS_TOKENS.add('struct')
CLASS_TOKENS.add('interface')
CLASS_TOKENS.add('trait')
CLASS_TOKENS.add('impl')
CLASS_TOKENS.add('enum')
CLASS_TOKENS.add('object')
CLASS_TOKENS.add('protocol')
CLASS_TOKENS.add('record')
CLASS_TOKENS.add('union')
CLASS_TOKENS.add('contract')
CLASS_TOKENS.add('module')
CLASS_TOKENS.add('mod')
CLASS_TOKENS.add('namespace')
CLASS_TOKENS.add('mixin')
CLASS_TOKENS.add('extension')
CLASS_TOKENS.add('codeunit')
CLASS_TOKENS.add('actor')
CLASS_TOKENS.add('package')

CLASS_EXACT = set()
CLASS_EXACT.add('package_body')

NOT_CLASS_TOKENS = set()
NOT_CLASS_TOKENS.add('name')
NOT_CLASS_TOKENS.add('identifier')
NOT_CLASS_TOKENS.add('body')
NOT_CLASS_TOKENS.add('list')
NOT_CLASS_TOKENS.add('reference')
NOT_CLASS_TOKENS.add('call')
NOT_CLASS_TOKENS.add('expression')
NOT_CLASS_TOKENS.add('pattern')
NOT_CLASS_TOKENS.add('literal')
NOT_CLASS_TOKENS.add('keyword')
NOT_CLASS_TOKENS.add('modifier')
NOT_CLASS_TOKENS.add('modifiers')
NOT_CLASS_TOKENS.add('parameter')
NOT_CLASS_TOKENS.add('parameters')
NOT_CLASS_TOKENS.add('argument')
NOT_CLASS_TOKENS.add('arguments')
NOT_CLASS_TOKENS.add('member')
NOT_CLASS_TOKENS.add('variant')
NOT_CLASS_TOKENS.add('constant')
NOT_CLASS_TOKENS.add('entry')
NOT_CLASS_TOKENS.add('field')
NOT_CLASS_TOKENS.add('access')
NOT_CLASS_TOKENS.add('import')
NOT_CLASS_TOKENS.add('export')
NOT_CLASS_TOKENS.add('path')
NOT_CLASS_TOKENS.add('header')
NOT_CLASS_TOKENS.add('heritage')
NOT_CLASS_TOKENS.add('clause')
NOT_CLASS_TOKENS.add('attribute')
NOT_CLASS_TOKENS.add('spec')
NOT_CLASS_TOKENS.add('elem')
NOT_CLASS_TOKENS.add('elements')
# `x_or_y` node types are grammar unions (verilog's module_or_generate_item),
# never a class themselves
NOT_CLASS_TOKENS.add('or')
NOT_CLASS_TOKENS.add('property')

NOT_CLASS_EXACT = set()
NOT_CLASS_EXACT.add('object')
NOT_CLASS_EXACT.add('module')

CALL_TOKENS = set()
CALL_TOKENS.add('call')
CALL_TOKENS.add('invocation')
CALL_TOKENS.add('application')
CALL_TOKENS.add('apply')

NOT_CALL_TOKENS = set()
NOT_CALL_TOKENS.add('arguments')
NOT_CALL_TOKENS.add('argument')
NOT_CALL_TOKENS.add('suffix')
NOT_CALL_TOKENS.add('macro')
NOT_CALL_TOKENS.add('type')
NOT_CALL_TOKENS.add('signature')
NOT_CALL_TOKENS.add('operator')

# subtrees never searched for a mentioned name: a comment or a string can spell
# anything, and a signature spells the function's own name and its parameters
NOT_MENTION_TOKENS = set()
NOT_MENTION_TOKENS.add('comment')
NOT_MENTION_TOKENS.add('string')
NOT_MENTION_TOKENS.add('char')
NOT_MENTION_TOKENS.add('parameter')
NOT_MENTION_TOKENS.add('parameters')
NOT_MENTION_TOKENS.add('param')
NOT_MENTION_TOKENS.add('params')
NOT_MENTION_TOKENS.add('type')

CALLEE_FIELDS = []
CALLEE_FIELDS.append('function')
CALLEE_FIELDS.append('target')
CALLEE_FIELDS.append('expr')
CALLEE_FIELDS.append('callee')
CALLEE_FIELDS.append('name')
CALLEE_FIELDS.append('method')
CALLEE_FIELDS.append('fun')

NAME_TOKENS = set()
NAME_TOKENS.add('identifier')
NAME_TOKENS.add('name')
NAME_TOKENS.add('symbol')
NAME_TOKENS.add('sym')
NAME_TOKENS.add('ident')
NAME_TOKENS.add('variable')
NAME_TOKENS.add('atom')
NAME_TOKENS.add('constant')
NAME_TOKENS.add('word')

# never followed when hunting for a declared name: a return type is not one
NOT_NAME_TOKENS = set()
NOT_NAME_TOKENS.add('type')

# a child carrying one of these holds names but is not the name: fortran's
# `variable_declaration` ("integer :: value, r") is a NAME_TOKENS match too
NOT_NAME_CHILD_TOKENS = set()
NOT_NAME_CHILD_TOKENS.add('type')
NOT_NAME_CHILD_TOKENS.add('declaration')
NOT_NAME_CHILD_TOKENS.add('statement')
NOT_NAME_CHILD_TOKENS.add('body')
NOT_NAME_CHILD_TOKENS.add('block')

LISP_FORM_TYPES = set()
LISP_FORM_TYPES.add('list')
LISP_FORM_TYPES.add('list_lit')
LISP_FORM_TYPES.add('call')
LISP_FORM_TYPES.add('tuple')

LISP_DEF_WORDS = set()
LISP_DEF_WORDS.add('def')
LISP_DEF_WORDS.add('defp')
LISP_DEF_WORDS.add('defn')
LISP_DEF_WORDS.add('defn-')
LISP_DEF_WORDS.add('defun')
LISP_DEF_WORDS.add('defmacro')
LISP_DEF_WORDS.add('defmacrop')
LISP_DEF_WORDS.add('defmacro-')
LISP_DEF_WORDS.add('defmethod')
LISP_DEF_WORDS.add('defguard')
LISP_DEF_WORDS.add('defguardp')
LISP_DEF_WORDS.add('defdelegate')
LISP_DEF_WORDS.add('defsubst')
LISP_DEF_WORDS.add('defgeneric')
LISP_DEF_WORDS.add('cl-defun')
LISP_DEF_WORDS.add('cl-defmacro')
LISP_DEF_WORDS.add('cl-defmethod')
LISP_DEF_WORDS.add('cl-defgeneric')
LISP_DEF_WORDS.add('define')
LISP_DEF_WORDS.add('define-public')
LISP_DEF_WORDS.add('define-private')
LISP_DEF_WORDS.add('define-read-only')
LISP_DEF_WORDS.add('define-syntax')
LISP_DEF_WORDS.add('define-macro')
LISP_DEF_WORDS.add('define-inline')
LISP_DEF_WORDS.add('define-method')
LISP_DEF_WORDS.add('defwidget')
LISP_DEF_WORDS.add('defroutes')
LISP_DEF_WORDS.add('deftest')

LISP_ANONYMOUS_WORDS = set()
LISP_ANONYMOUS_WORDS.add('fn')
LISP_ANONYMOUS_WORDS.add('fn*')
LISP_ANONYMOUS_WORDS.add('lambda')
LISP_ANONYMOUS_WORDS.add('λ')
LISP_ANONYMOUS_WORDS.add('function')

LISP_DEF_WORDS_NEED_LIST = set()
LISP_DEF_WORDS_NEED_LIST.add('define')

LISP_CLASS_WORDS = set()
LISP_CLASS_WORDS.add('defmodule')
LISP_CLASS_WORDS.add('defprotocol')
LISP_CLASS_WORDS.add('defimpl')
LISP_CLASS_WORDS.add('defrecord')
LISP_CLASS_WORDS.add('deftype')
LISP_CLASS_WORDS.add('defstruct')
LISP_CLASS_WORDS.add('defclass')
LISP_CLASS_WORDS.add('defmodule')
LISP_CLASS_WORDS.add('define-record-type')
LISP_CLASS_WORDS.add('define-class')
LISP_CLASS_WORDS.add('ns')

ML_BINDING_TYPES = set()
ML_BINDING_TYPES.add('let_binding')
ML_BINDING_TYPES.add('value_declaration')
ML_BINDING_TYPES.add('value_definition')
ML_BINDING_TYPES.add('binding')
ML_BINDING_TYPES.add('let')

ML_PARAMETER_TOKENS = set()
ML_PARAMETER_TOKENS.add('parameter')
ML_PARAMETER_TOKENS.add('parameters')
ML_PARAMETER_TOKENS.add('param')
ML_PARAMETER_TOKENS.add('function')
ML_PARAMETER_TOKENS.add('call')

WRAPPER_TOKENS = set()
WRAPPER_TOKENS.add('declaration')
WRAPPER_TOKENS.add('declarator')
WRAPPER_TOKENS.add('binding')
WRAPPER_TOKENS.add('assignment')
WRAPPER_TOKENS.add('definition')
WRAPPER_TOKENS.add('let')
WRAPPER_TOKENS.add('pair')
WRAPPER_TOKENS.add('property')
WRAPPER_TOKENS.add('field')
WRAPPER_TOKENS.add('variable')
WRAPPER_TOKENS.add('export')
WRAPPER_TOKENS.add('spec')
WRAPPER_TOKENS.add('type')

WRAPPER_STOP_TOKENS = set()
WRAPPER_STOP_TOKENS.add('block')
WRAPPER_STOP_TOKENS.add('body')
WRAPPER_STOP_TOKENS.add('class')
WRAPPER_STOP_TOKENS.add('struct')
WRAPPER_STOP_TOKENS.add('impl')
WRAPPER_STOP_TOKENS.add('interface')
WRAPPER_STOP_TOKENS.add('trait')
WRAPPER_STOP_TOKENS.add('module')
WRAPPER_STOP_TOKENS.add('program')
WRAPPER_STOP_TOKENS.add('file')
WRAPPER_STOP_TOKENS.add('unit')
WRAPPER_STOP_TOKENS.add('source')
WRAPPER_STOP_TOKENS.add('chunk')

EMBEDDED_SCRIPT_TYPES = set()
EMBEDDED_SCRIPT_TYPES.add('raw_text')
EMBEDDED_SCRIPT_TYPES.add('frontmatter_js_block')


_tokens = {}


def type_tokens(node_type):
    """the words in a node type name, cached

    a grammar has a few hundred node types and every classification asks for
    the same split again; the regex was a fifth of the time spent indexing.
    the returned set is shared, so callers must not change it.
    """
    found = _tokens.get(node_type)
    if found is not None: return found
    spaced = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', node_type)
    tokens = set()
    for token in spaced.lower().split('_'):
        if not token: continue
        tokens.add(token)
    _tokens[node_type] = tokens
    return tokens


def text_of(node, source):
    return source[node.start_byte:node.end_byte].decode('utf-8', 'replace')


def first_word(node, source):
    for child in node.named_children:
        return text_of(child, source).strip()
    return ''


def second_named_child(node):
    index = 0
    for child in node.named_children:
        index = index + 1
        if index < 2: continue
        return child
    return None


def is_lisp_definition(node, source):
    if node.type not in LISP_FORM_TYPES: return False
    word = first_word(node, source)
    if word in LISP_ANONYMOUS_WORDS: return True
    if word not in LISP_DEF_WORDS: return False
    if word not in LISP_DEF_WORDS_NEED_LIST: return True
    second = second_named_child(node)
    if second is None: return False
    return second.type in LISP_FORM_TYPES


def is_lisp_anonymous(node, source):
    if node.type not in LISP_FORM_TYPES: return False
    return first_word(node, source) in LISP_ANONYMOUS_WORDS


def is_lisp_class(node, source):
    if node.type not in LISP_FORM_TYPES: return False
    return first_word(node, source) in LISP_CLASS_WORDS


def is_lisp_call(node, source):
    if node.type not in LISP_FORM_TYPES: return False
    if is_lisp_definition(node, source): return False
    if is_lisp_class(node, source): return False
    for child in node.named_children:
        return bool(type_tokens(child.type) & {'symbol', 'sym', 'identifier'})
    return False


def is_ml_function(node):
    if node.type not in ML_BINDING_TYPES: return False
    for child in node.named_children:
        if type_tokens(child.type) & ML_PARAMETER_TOKENS: return True
    return False


def is_inner_body(node, source):
    """a body belonging to a definition around it, rather than a definition itself

    the same type name means opposite things across grammars: d hangs
    `function_body` under its `function_declaration`, dart puts it next to a
    `function_signature`, vhdl's *is* the whole subprogram. the neighbours
    settle it.
    """
    if node.type not in INNER_BODY_TYPES: return False
    parent = node.parent
    if parent is not None and is_function_node(parent, source): return True
    previous = node.prev_named_sibling
    if previous is None: return False
    return 'signature' in previous.type


def owns_body(node):
    for child in node.named_children:
        if child.type in INNER_BODY_TYPES: return True
        if type_tokens(child.type) & BODY_TOKENS: return True
    return False


def is_function_node(node, source):
    if not node.is_named: return False
    if node.type in FUNCTION_EXACT: return True
    if is_inner_body(node, source): return False
    if is_lisp_definition(node, source): return True
    if is_ml_function(node): return True
    tokens = type_tokens(node.type)
    if 'decorated' in tokens: return False
    # only the first child: zig writes `Decl (FnProto) (Block)`, and walking
    # every child cost a millisecond a call on a file with many definitions
    if node.named_child_count:
        first = node.named_child(0)
        if first is not None and first.type in HEADER_CHILD_TYPES: return True
    if tokens & NOT_FUNCTION_TOKENS: return False
    return bool(tokens & FUNCTION_TOKENS)


def is_anonymous_node(node, source):
    if is_lisp_anonymous(node, source): return True
    return bool(type_tokens(node.type) & ANONYMOUS_TOKENS)


def at_top(node):
    """the tree root, or a direct child of it"""
    parent = node.parent
    if parent is None: return True
    if parent.type == 'program': return True
    return parent.parent is None


def is_class_node(node, source):
    if not node.is_named: return False
    if node.type in CLASS_EXACT: return True
    if node.type in NOT_CLASS_EXACT and not at_top(node): return False
    if is_lisp_class(node, source): return True
    tokens = type_tokens(node.type)
    if 'decorated' in tokens: return False
    if tokens & NOT_CLASS_TOKENS: return False
    return bool(tokens & CLASS_TOKENS)


def veto_tokens(node_type):
    """the tokens a reject list may act on

    a `x_or_y` node type is a grammar union, and inherits no veto from either
    branch: wgsl calls its call node
    `type_constructor_or_function_call_expression`, which is a call however
    much the word `type` appears in it.
    """
    tokens = type_tokens(node_type)
    if 'or' in tokens: return set()
    return tokens


def is_call_node(node, source):
    if not node.is_named: return False
    if is_lisp_call(node, source): return True
    if veto_tokens(node.type) & NOT_CALL_TOKENS: return False
    return bool(type_tokens(node.type) & CALL_TOKENS)


def ancestors(node):
    chain = []
    while node is not None:
        chain.append(node)
        node = node.parent
    return chain


def descendants(root):
    """every node under root (root included), depth first"""
    cursor = root.walk()
    while True:
        yield cursor.node
        if cursor.goto_first_child(): continue
        if cursor.goto_next_sibling(): continue
        climbing = True
        while climbing:
            if not cursor.goto_parent(): return
            if cursor.goto_next_sibling(): climbing = False


def with_names(nodes, source):
    """only the candidates that declare a name, unless none of them do"""
    kept = []
    for node in nodes:
        if name_of(node, source) is None: continue
        kept.append(node)
    if not kept: return nodes
    return kept


def with_bodies(nodes):
    """only the candidates that own a body, unless none of them do"""
    kept = []
    for node in nodes:
        if not owns_body(node): continue
        kept.append(node)
    if not kept: return nodes
    return kept


def widest_at_row(nodes):
    """the outermost of the run starting on the innermost candidate's row

    grammars stack a definition, its signature and its keyword on one row, and
    the innermost of those is a fragment. a real enclosing function starts on
    an earlier row, so the run stops before it.
    """
    row = nodes[0].start_point.row
    found = nodes[0]
    for node in nodes:
        if node.start_point.row != row: break
        found = node
    return found


def pick_function(leaf, source, mode):
    named = []
    every = []
    for node in ancestors(leaf):
        if not is_function_node(node, source): continue
        every.append(node)
        if is_anonymous_node(node, source): continue
        named.append(node)
    if not every: return None
    if mode == 'outer': return every[-1]
    if mode == 'inner': return every[0]
    if not named: return every[-1]
    return widest_at_row(with_bodies(with_names(named, source)))


def pick_class(leaf, source, mode):
    every = []
    for node in ancestors(leaf):
        if not is_class_node(node, source): continue
        every.append(node)
    if not every: return None
    if mode == 'outer': return every[-1]
    # a declaration line names the class without being it: smali's
    # `.class public final Lp/dv91;` is a class_directive inside the
    # class_definition that is the whole file, and both start on row one
    return widest_at_row(every)


def is_inner_duplicate(node, source):
    """a function node another function node already covers, on the same row

    grammars that split a definition into a body plus a signature (plus a
    keyword marker) yield two or three function nodes per definition. only the
    outermost of that run is the definition.
    """
    parent = node.parent
    while parent is not None:
        if parent.start_point.row != node.start_point.row: return False
        if is_function_node(parent, source): return True
        parent = parent.parent
    return False


def is_nested_fragment(node, source):
    """a bodyless function node written inside another function

    smali's invoke line parses as a `full_method_signature`, which carries the
    callee's name and reads exactly like a definition. a real definition
    nested in another one still owns its body.
    """
    if 'signature' not in node.type: return False
    if owns_body(node): return False
    parent = node.parent
    while parent is not None:
        if is_function_node(parent, source): return True
        parent = parent.parent
    return False


def pick_fallback_class(leaf, source, mode):
    """the class to show when nothing encloses the hit as a function

    narrower than pick_class on purpose. a file's own root counts as a class
    for --class, and in smali that is the whole answer: the file is one
    class, so a hit on a directive or a field has nowhere else to go. but a
    stray top-level line in python would drag in the entire module, which is
    worse than leaving the line alone, and NOT_CLASS_EXACT is exactly the set
    of types that are a class only by virtue of sitting at the top.
    """
    node = pick_class(leaf, source, mode)
    if node is None: return None
    if node.type in NOT_CLASS_EXACT: return None
    return node


def climb_wrappers(node):
    while True:
        parent = node.parent
        if parent is None: return node
        if 'decorated' in type_tokens(parent.type): return parent
        if parent.start_point.row != node.start_point.row: return node
        tokens = type_tokens(parent.type)
        if not tokens & WRAPPER_TOKENS: return node
        if tokens & WRAPPER_STOP_TOKENS: return node
        if 'list' in tokens and parent.type != 'expression_list': return node
        node = parent


def pick_body_with_signature(leaf):
    for node in ancestors(leaf):
        if node.type not in INNER_BODY_TYPES: continue
        previous = node.prev_named_sibling
        if previous is None: continue
        if 'signature' not in previous.type: continue
        return node
    return None


def widen(node):
    while node.parent is not None and 'signature' in node.parent.type:
        node = node.parent
    start = node
    end = node
    if node.type in INNER_BODY_TYPES:
        previous = node.prev_named_sibling
        if previous is not None and 'signature' in previous.type: start = previous
    if 'signature' in node.type:
        following = node.next_named_sibling
        if following is not None and following.type in INNER_BODY_TYPES: end = following
    return start, end


def rows_of(node):
    start, end = widen(node)
    return start.start_point.row, end.end_point.row


def leaf_at(root, row, col):
    return root.descendant_for_point_range((row, col), (row, col + 1))


def embedded_script(leaf):
    for node in ancestors(leaf):
        if node.type in EMBEDDED_SCRIPT_TYPES: return node
    return None


def first_name_leaf(node):
    for child in descendants(node):
        if not child.is_named: continue
        if child.named_child_count: continue
        if type_tokens(child.type) & NAME_TOKENS: return child
    return None


def last_name_leaf(node):
    found = None
    for child in descendants(node):
        if not child.is_named: continue
        if child.named_child_count: continue
        if type_tokens(child.type) & NAME_TOKENS: found = child
    return found


def is_name_child(node):
    """a child that is the declared name itself, not a construct holding names"""
    tokens = type_tokens(node.type)
    if not tokens & NAME_TOKENS: return False
    return not tokens & NOT_NAME_CHILD_TOKENS


def name_of(node, source):
    """the declared name of a function/class node, or None"""
    named = node.child_by_field_name('name')
    if named is not None:
        leaf = last_name_leaf(named)
        if leaf is None: return text_of(named, source).strip()
        return text_of(leaf, source)
    if node.type in LISP_FORM_TYPES:
        second = second_named_child(node)
        if second is None: return None
        leaf = first_name_leaf(second)
        if leaf is None: return None
        return text_of(leaf, source)
    for child in node.named_children:
        if not is_name_child(child): continue
        leaf = last_name_leaf(child)
        if leaf is None: return text_of(child, source).strip()
        return text_of(leaf, source)
    for child in node.named_children:
        tokens = type_tokens(child.type)
        if tokens & NOT_NAME_TOKENS: continue
        nested = False
        if is_function_node(child, source): nested = True
        if is_class_node(child, source): nested = True
        if child.type in HEADER_CHILD_TYPES: nested = True
        if tokens & WRAPPER_TOKENS and not tokens & WRAPPER_STOP_TOKENS: nested = True
        if 'decorated' in tokens: nested = True
        if not nested: continue
        found = name_of(child, source)
        if found is not None: return found
    leaf = first_name_leaf(node)
    if leaf is None: return None
    return text_of(leaf, source)


def callee_name(call, source):
    target = None
    for field in CALLEE_FIELDS:
        target = call.child_by_field_name(field)
        if target is not None: break
    if target is None:
        for child in call.named_children:
            target = child
            break
    if target is None: return None
    leaf = last_name_leaf(target)
    if leaf is None:
        if target.named_child_count: return None
        return text_of(target, source).strip()
    return text_of(leaf, source)


def calls_in(node, source):
    names = set()
    for child in descendants(node):
        if not is_call_node(child, source): continue
        name = callee_name(child, source)
        if not name: continue
        names.add(name)
    return names


def mention_leaves(node):
    """named leaves under node, with comment, string and signature subtrees pruned"""
    found = []
    stack = []
    for child in node.named_children:
        stack.append(child)
    while stack:
        current = stack.pop()
        if veto_tokens(current.type) & NOT_MENTION_TOKENS: continue
        if not current.named_child_count:
            found.append(current)
            continue
        for child in current.named_children:
            stack.append(child)
    return found


def mentions_in(node, source, known, own):
    """names out of `known` written inside node, for grammars with no call node

    most grammars give a call a node type of its own, and is_call_node finds it
    by that name. a good many do not: bash runs `helper "$1"` as a plain
    command, wat writes `call $helper` as an instruction, smali's invoke is a
    bare expression. there is no node type to match on, but every one of them
    still spells the callee out, so a name that is indexed and written in the
    body is taken as a call. the function's own name does not count, which
    drops self-recursion along with the signature.
    """
    names = set()
    for leaf in mention_leaves(node):
        text = text_of(leaf, source).strip()
        if not text: continue
        if text == own: continue
        if text not in known: continue
        names.add(text)
    return names


def find_definition(root, source, row, col, args):
    """the function (or class) node around the hit, or None"""
    leaf = leaf_at(root, row, col)
    if leaf is None: return None
    if args.kind == 'class':
        node = pick_class(leaf, source, args.mode)
        if node is None: return None
        return climb_wrappers(node)
    node = pick_function(leaf, source, args.mode)
    if node is not None: return climb_wrappers(node)
    node = pick_body_with_signature(leaf)
    if node is not None: return node
    node = pick_fallback_class(leaf, source, args.mode)
    if node is None: return None
    return climb_wrappers(node)

