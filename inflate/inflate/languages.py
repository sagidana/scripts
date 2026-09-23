"""grammar picking and parsing: which tree-sitter language a file is, and its tree"""

import os
import re
import sys

import tree_sitter_language_pack


EXTENSIONS = {}
EXTENSIONS['.py'] = 'python'
EXTENSIONS['.pyi'] = 'python'
EXTENSIONS['.pyw'] = 'python'
EXTENSIONS['.gyp'] = 'python'
EXTENSIONS['.bzl'] = 'starlark'
EXTENSIONS['.star'] = 'starlark'
EXTENSIONS['.mojo'] = 'mojo'
EXTENSIONS['.js'] = 'javascript'
EXTENSIONS['.mjs'] = 'javascript'
EXTENSIONS['.cjs'] = 'javascript'
EXTENSIONS['.jsx'] = 'javascript'
EXTENSIONS['.ts'] = 'typescript'
EXTENSIONS['.mts'] = 'typescript'
EXTENSIONS['.cts'] = 'typescript'
EXTENSIONS['.tsx'] = 'tsx'
EXTENSIONS['.vue'] = 'vue'
EXTENSIONS['.svelte'] = 'svelte'
EXTENSIONS['.astro'] = 'astro'
EXTENSIONS['.qml'] = 'qmljs'
EXTENSIONS['.res'] = 'rescript'
EXTENSIONS['.go'] = 'go'
EXTENSIONS['.templ'] = 'templ'
EXTENSIONS['.mod'] = 'gomod'
EXTENSIONS['.sum'] = 'gosum'
EXTENSIONS['.rs'] = 'rust'
EXTENSIONS['.c'] = 'c'
EXTENSIONS['.h'] = 'c'
EXTENSIONS['.cc'] = 'cpp'
EXTENSIONS['.cpp'] = 'cpp'
EXTENSIONS['.cxx'] = 'cpp'
EXTENSIONS['.c++'] = 'cpp'
EXTENSIONS['.hh'] = 'cpp'
EXTENSIONS['.hpp'] = 'cpp'
EXTENSIONS['.hxx'] = 'cpp'
EXTENSIONS['.h++'] = 'cpp'
EXTENSIONS['.ipp'] = 'cpp'
EXTENSIONS['.tpp'] = 'cpp'
EXTENSIONS['.ino'] = 'arduino'
EXTENSIONS['.cu'] = 'cuda'
EXTENSIONS['.cuh'] = 'cuda'
EXTENSIONS['.ispc'] = 'ispc'
EXTENSIONS['.m'] = 'objc'
EXTENSIONS['.mm'] = 'objc'
EXTENSIONS['.java'] = 'java'
EXTENSIONS['.kt'] = 'kotlin'
EXTENSIONS['.kts'] = 'kotlin'
EXTENSIONS['.scala'] = 'scala'
EXTENSIONS['.sc'] = 'scala'
EXTENSIONS['.groovy'] = 'groovy'
EXTENSIONS['.gradle'] = 'groovy'
EXTENSIONS['.cs'] = 'csharp'
EXTENSIONS['.vb'] = 'vb'
EXTENSIONS['.fs'] = 'fsharp'
EXTENSIONS['.fsx'] = 'fsharp'
EXTENSIONS['.fsi'] = 'fsharp_signature'
EXTENSIONS['.swift'] = 'swift'
EXTENSIONS['.dart'] = 'dart'
EXTENSIONS['.rb'] = 'ruby'
EXTENSIONS['.rake'] = 'ruby'
EXTENSIONS['.gemspec'] = 'ruby'
EXTENSIONS['.cr'] = 'crystal'
EXTENSIONS['.php'] = 'php'
EXTENSIONS['.phtml'] = 'php'
EXTENSIONS['.hack'] = 'hack'
EXTENSIONS['.pl'] = 'perl'
EXTENSIONS['.pm'] = 'perl'
EXTENSIONS['.t'] = 'perl'
EXTENSIONS['.lua'] = 'lua'
EXTENSIONS['.luau'] = 'luau'
EXTENSIONS['.tl'] = 'teal'
EXTENSIONS['.fnl'] = 'fennel'
EXTENSIONS['.gd'] = 'gdscript'
EXTENSIONS['.tres'] = 'godot_resource'
EXTENSIONS['.tscn'] = 'godot_resource'
EXTENSIONS['.sh'] = 'bash'
EXTENSIONS['.bash'] = 'bash'
EXTENSIONS['.zsh'] = 'zsh'
EXTENSIONS['.fish'] = 'fish'
EXTENSIONS['.nu'] = 'nushell'
EXTENSIONS['.ps1'] = 'powershell'
EXTENSIONS['.psm1'] = 'powershell'
EXTENSIONS['.psd1'] = 'powershell'
EXTENSIONS['.bat'] = 'batch'
EXTENSIONS['.cmd'] = 'batch'
EXTENSIONS['.awk'] = 'awk'
EXTENSIONS['.tcl'] = 'tcl'
EXTENSIONS['.exp'] = 'tcl'
EXTENSIONS['.vim'] = 'vim'
EXTENSIONS['.ex'] = 'elixir'
EXTENSIONS['.exs'] = 'elixir'
EXTENSIONS['.heex'] = 'heex'
EXTENSIONS['.eex'] = 'eex'
EXTENSIONS['.erl'] = 'erlang'
EXTENSIONS['.hrl'] = 'erlang'
EXTENSIONS['.gleam'] = 'gleam'
EXTENSIONS['.hs'] = 'haskell'
EXTENSIONS['.lhs'] = 'haskell'
EXTENSIONS['.purs'] = 'purescript'
EXTENSIONS['.elm'] = 'elm'
EXTENSIONS['.ml'] = 'ocaml'
EXTENSIONS['.mli'] = 'ocaml_interface'
EXTENSIONS['.agda'] = 'agda'
EXTENSIONS['.idr'] = 'idris'
EXTENSIONS['.lean'] = 'lean'
EXTENSIONS['.clj'] = 'clojure'
EXTENSIONS['.cljs'] = 'clojure'
EXTENSIONS['.cljc'] = 'clojure'
EXTENSIONS['.edn'] = 'clojure'
EXTENSIONS['.el'] = 'elisp'
EXTENSIONS['.lisp'] = 'commonlisp'
EXTENSIONS['.cl'] = 'commonlisp'
EXTENSIONS['.asd'] = 'commonlisp'
EXTENSIONS['.scm'] = 'scheme'
EXTENSIONS['.ss'] = 'scheme'
EXTENSIONS['.sld'] = 'scheme'
EXTENSIONS['.rkt'] = 'racket'
EXTENSIONS['.janet'] = 'janet'
EXTENSIONS['.bass'] = 'bass'
EXTENSIONS['.yuck'] = 'yuck'
EXTENSIONS['.clar'] = 'clarity'
EXTENSIONS['.zig'] = 'zig'
EXTENSIONS['.odin'] = 'odin'
EXTENSIONS['.v'] = 'v'
EXTENSIONS['.vsh'] = 'v'
EXTENSIONS['.d'] = 'd'
EXTENSIONS['.nim'] = 'nim'
EXTENSIONS['.nims'] = 'nim'
EXTENSIONS['.ha'] = 'hare'
EXTENSIONS['.pony'] = 'pony'
EXTENSIONS['.hx'] = 'haxe'
EXTENSIONS['.nut'] = 'squirrel'
EXTENSIONS['.cairo'] = 'cairo'
EXTENSIONS['.move'] = 'move'
EXTENSIONS['.sol'] = 'solidity'
EXTENSIONS['.fc'] = 'func'
EXTENSIONS['.circom'] = 'circom'
EXTENSIONS['.jl'] = 'julia'
EXTENSIONS['.r'] = 'r'
EXTENSIONS['.R'] = 'r'
EXTENSIONS['.rmd'] = 'r'
EXTENSIONS['.f'] = 'fortran'
EXTENSIONS['.f90'] = 'fortran'
EXTENSIONS['.f95'] = 'fortran'
EXTENSIONS['.f03'] = 'fortran'
EXTENSIONS['.f08'] = 'fortran'
EXTENSIONS['.for'] = 'fortran'
EXTENSIONS['.pas'] = 'pascal'
EXTENSIONS['.pp'] = 'pascal'
EXTENSIONS['.dpr'] = 'pascal'
EXTENSIONS['.ada'] = 'ada'
EXTENSIONS['.adb'] = 'ada'
EXTENSIONS['.ads'] = 'ada'
EXTENSIONS['.cob'] = 'cobol'
EXTENSIONS['.cbl'] = 'cobol'
EXTENSIONS['.cpy'] = 'cobol'
EXTENSIONS['.bsl'] = 'bsl'
EXTENSIONS['.os'] = 'bsl'
EXTENSIONS['.al'] = 'al'
EXTENSIONS['.magik'] = 'magik'
EXTENSIONS['.pro'] = 'prolog'
EXTENSIONS['.prolog'] = 'prolog'
EXTENSIONS['.cls'] = 'apex'
EXTENSIONS['.trigger'] = 'apex'
EXTENSIONS['.brs'] = 'brightscript'
EXTENSIONS['.axs'] = 'netlinx'
EXTENSIONS['.axi'] = 'netlinx'
EXTENSIONS['.nqc'] = 'nqc'
EXTENSIONS['.4th'] = 'forth'
EXTENSIONS['.forth'] = 'forth'
EXTENSIONS['.fth'] = 'forth'
EXTENSIONS['.tal'] = 'uxntal'
EXTENSIONS['.smali'] = 'smali'
EXTENSIONS['.ll'] = 'llvm'
EXTENSIONS['.td'] = 'tablegen'
EXTENSIONS['.asm'] = 'asm'
EXTENSIONS['.s'] = 'asm'
EXTENSIONS['.S'] = 'asm'
EXTENSIONS['.wat'] = 'wat'
EXTENSIONS['.wast'] = 'wast'
EXTENSIONS['.wit'] = 'wit'
EXTENSIONS['.glsl'] = 'glsl'
EXTENSIONS['.vert'] = 'glsl'
EXTENSIONS['.frag'] = 'glsl'
EXTENSIONS['.geom'] = 'glsl'
EXTENSIONS['.comp'] = 'glsl'
EXTENSIONS['.hlsl'] = 'hlsl'
EXTENSIONS['.fx'] = 'hlsl'
EXTENSIONS['.wgsl'] = 'wgsl'
EXTENSIONS['.sv'] = 'verilog'
EXTENSIONS['.svh'] = 'verilog'
EXTENSIONS['.vh'] = 'verilog'
EXTENSIONS['.vhd'] = 'vhdl'
EXTENSIONS['.vhdl'] = 'vhdl'
EXTENSIONS['.fir'] = 'firrtl'
EXTENSIONS['.dsp'] = 'faust'
EXTENSIONS['.sql'] = 'sql'
EXTENSIONS['.psql'] = 'sql'
EXTENSIONS['.jq'] = 'jq'
EXTENSIONS['.ql'] = 'ql'
EXTENSIONS['.qll'] = 'ql'
EXTENSIONS['.rego'] = 'rego'
EXTENSIONS['.pkl'] = 'pkl'
EXTENSIONS['.typ'] = 'typst'
EXTENSIONS['.nix'] = 'nix'
EXTENSIONS['.cmake'] = 'cmake'
EXTENSIONS['.mk'] = 'make'
EXTENSIONS['.make'] = 'make'
EXTENSIONS['.ninja'] = 'ninja'
EXTENSIONS['.just'] = 'just'
EXTENSIONS['.earth'] = 'earthfile'
EXTENSIONS['.dockerfile'] = 'dockerfile'
EXTENSIONS['.tf'] = 'terraform'
EXTENSIONS['.tfvars'] = 'terraform'
EXTENSIONS['.hcl'] = 'hcl'
EXTENSIONS['.nomad'] = 'hcl'
EXTENSIONS['.bicep'] = 'bicep'
EXTENSIONS['.cue'] = 'cue'
EXTENSIONS['.kdl'] = 'kdl'
EXTENSIONS['.jsonnet'] = 'jsonnet'
EXTENSIONS['.libsonnet'] = 'jsonnet'
EXTENSIONS['.ron'] = 'ron'
EXTENSIONS['.toml'] = 'toml'
EXTENSIONS['.yaml'] = 'yaml'
EXTENSIONS['.yml'] = 'yaml'
EXTENSIONS['.json'] = 'json'
EXTENSIONS['.jsonc'] = 'json'
EXTENSIONS['.json5'] = 'json'
EXTENSIONS['.xml'] = 'xml'
EXTENSIONS['.xsd'] = 'xml'
EXTENSIONS['.svg'] = 'xml'
EXTENSIONS['.plist'] = 'xml'
EXTENSIONS['.dtd'] = 'dtd'
EXTENSIONS['.html'] = 'html'
EXTENSIONS['.htm'] = 'html'
EXTENSIONS['.css'] = 'css'
EXTENSIONS['.scss'] = 'scss'
EXTENSIONS['.less'] = 'less'
EXTENSIONS['.pug'] = 'pug'
EXTENSIONS['.twig'] = 'twig'
EXTENSIONS['.liquid'] = 'liquid'
EXTENSIONS['.j2'] = 'jinja2'
EXTENSIONS['.jinja'] = 'jinja2'
EXTENSIONS['.jinja2'] = 'jinja2'
EXTENSIONS['.md'] = 'markdown'
EXTENSIONS['.markdown'] = 'markdown'
EXTENSIONS['.rst'] = 'rst'
EXTENSIONS['.org'] = 'org'
EXTENSIONS['.norg'] = 'norg'
EXTENSIONS['.tex'] = 'latex'
EXTENSIONS['.sty'] = 'latex'
EXTENSIONS['.bib'] = 'bibtex'
EXTENSIONS['.adoc'] = 'asciidoc'
EXTENSIONS['.dj'] = 'djot'
EXTENSIONS['.proto'] = 'proto'
EXTENSIONS['.thrift'] = 'thrift'
EXTENSIONS['.fidl'] = 'fidl'
EXTENSIONS['.capnp'] = 'capnp'
EXTENSIONS['.smithy'] = 'smithy'
EXTENSIONS['.graphql'] = 'graphql'
EXTENSIONS['.gql'] = 'graphql'
EXTENSIONS['.prisma'] = 'prisma'
EXTENSIONS['.textproto'] = 'textproto'
EXTENSIONS['.pbtxt'] = 'textproto'
EXTENSIONS['.ebnf'] = 'ebnf'
EXTENSIONS['.ungram'] = 'ungrammar'
EXTENSIONS['.dot'] = 'dot'
EXTENSIONS['.gv'] = 'dot'
EXTENSIONS['.mmd'] = 'mermaid'
EXTENSIONS['.mermaid'] = 'mermaid'
EXTENSIONS['.dts'] = 'devicetree'
EXTENSIONS['.dtsi'] = 'devicetree'
EXTENSIONS['.ld'] = 'linkerscript'
EXTENSIONS['.lds'] = 'linkerscript'
EXTENSIONS['.bb'] = 'bitbake'
EXTENSIONS['.bbappend'] = 'bitbake'
EXTENSIONS['.bbclass'] = 'bitbake'
EXTENSIONS['.re'] = 're2c'
EXTENSIONS['.ini'] = 'ini'
EXTENSIONS['.cfg'] = 'ini'
EXTENSIONS['.conf'] = 'ini'
EXTENSIONS['.properties'] = 'properties'
EXTENSIONS['.desktop'] = 'desktop'
EXTENSIONS['.service'] = 'ini'
EXTENSIONS['.rules'] = 'udev'
EXTENSIONS['.gitignore'] = 'gitignore'
EXTENSIONS['.gitattributes'] = 'gitattributes'
EXTENSIONS['.editorconfig'] = 'editorconfig'
EXTENSIONS['.diff'] = 'diff'
EXTENSIONS['.patch'] = 'diff'
EXTENSIONS['.csv'] = 'csv'
EXTENSIONS['.tsv'] = 'tsv'
EXTENSIONS['.psv'] = 'psv'
EXTENSIONS['.pem'] = 'pem'
EXTENSIONS['.crt'] = 'pem'
EXTENSIONS['.po'] = 'po'
EXTENSIONS['.pot'] = 'po'
EXTENSIONS['.pgn'] = 'pgn'
EXTENSIONS['.ttl'] = 'turtle'
EXTENSIONS['.sparql'] = 'sparql'
EXTENSIONS['.rq'] = 'sparql'
EXTENSIONS['.http'] = 'http'
EXTENSIONS['.hurl'] = 'hurl'
EXTENSIONS['.cook'] = 'cooklang'
EXTENSIONS['.beancount'] = 'beancount'
EXTENSIONS['.ledger'] = 'ledger'
EXTENSIONS['.robot'] = 'robot'
EXTENSIONS['.chatito'] = 'chatito'
EXTENSIONS['.tla'] = 'tlaplus'
EXTENSIONS['.wl'] = 'wolfram'
EXTENSIONS['.wls'] = 'wolfram'
EXTENSIONS['.hyprlang'] = 'hyprlang'
EXTENSIONS['.cdc'] = 'cedar'
EXTENSIONS['.cedar'] = 'cedar'
EXTENSIONS['.cedarschema'] = 'cedarschema'
EXTENSIONS['.cylc'] = 'cylc'
EXTENSIONS['.corn'] = 'corn'
EXTENSIONS['.cpon'] = 'cpon'
EXTENSIONS['.nickel'] = 'nickel'
EXTENSIONS['.ncl'] = 'nickel'
EXTENSIONS['.gn'] = 'gn'
EXTENSIONS['.gni'] = 'gn'
EXTENSIONS['.kconfig'] = 'kconfig'
EXTENSIONS['.eds'] = 'eds'
EXTENSIONS['.gst'] = 'gstlaunch'
EXTENSIONS['.foam'] = 'foam'
EXTENSIONS['.xcompose'] = 'xcompose'
EXTENSIONS['.vimdoc'] = 'vimdoc'
EXTENSIONS['.query'] = 'query'
EXTENSIONS['.enforce'] = 'enforce'
EXTENSIONS['.c3'] = 'enforce'
EXTENSIONS['.mat'] = 'matlab'
EXTENSIONS['.m'] = 'objc'
FILENAMES = {}
FILENAMES['makefile'] = 'make'
FILENAMES['gnumakefile'] = 'make'
FILENAMES['dockerfile'] = 'dockerfile'
FILENAMES['containerfile'] = 'dockerfile'
FILENAMES['cmakelists.txt'] = 'cmake'
FILENAMES['justfile'] = 'just'
FILENAMES['meson.build'] = 'meson'
FILENAMES['meson_options.txt'] = 'meson'
FILENAMES['build'] = 'starlark'
FILENAMES['build.bazel'] = 'starlark'
FILENAMES['workspace'] = 'starlark'
FILENAMES['workspace.bazel'] = 'starlark'
FILENAMES['module.bazel'] = 'starlark'
FILENAMES['tiltfile'] = 'starlark'
FILENAMES['sconstruct'] = 'python'
FILENAMES['sconscript'] = 'python'
FILENAMES['earthfile'] = 'earthfile'
FILENAMES['caddyfile'] = 'caddy'
FILENAMES['jenkinsfile'] = 'groovy'
FILENAMES['rakefile'] = 'ruby'
FILENAMES['gemfile'] = 'ruby'
FILENAMES['guardfile'] = 'ruby'
FILENAMES['vagrantfile'] = 'ruby'
FILENAMES['podfile'] = 'ruby'
FILENAMES['brewfile'] = 'ruby'
FILENAMES['go.mod'] = 'gomod'
FILENAMES['go.sum'] = 'gosum'
FILENAMES['cargo.lock'] = 'toml'
FILENAMES['pipfile'] = 'toml'
FILENAMES['requirements.txt'] = 'requirements'
FILENAMES['manifest.in'] = 'pymanifest'
FILENAMES['.bashrc'] = 'bash'
FILENAMES['.bash_profile'] = 'bash'
FILENAMES['.bash_aliases'] = 'bash'
FILENAMES['.profile'] = 'bash'
FILENAMES['.zshrc'] = 'zsh'
FILENAMES['.zshenv'] = 'zsh'
FILENAMES['.zprofile'] = 'zsh'
FILENAMES['.vimrc'] = 'vim'
FILENAMES['.gvimrc'] = 'vim'
FILENAMES['init.vim'] = 'vim'
FILENAMES['.tmux.conf'] = 'tmux'
FILENAMES['.gitconfig'] = 'git_config'
FILENAMES['.gitmodules'] = 'git_config'
FILENAMES['.gitignore'] = 'gitignore'
FILENAMES['.gitattributes'] = 'gitattributes'
FILENAMES['.editorconfig'] = 'editorconfig'
FILENAMES['.inputrc'] = 'readline'
FILENAMES['ssh_config'] = 'ssh_config'
FILENAMES['sshd_config'] = 'ssh_config'
FILENAMES['nginx.conf'] = 'nginx'
FILENAMES['todo.txt'] = 'todotxt'
FILENAMES['.emacs'] = 'elisp'
FILENAMES['.clang-format'] = 'yaml'

SHEBANGS = {}
SHEBANGS['python'] = 'python'
SHEBANGS['python2'] = 'python'
SHEBANGS['python3'] = 'python'
SHEBANGS['sh'] = 'bash'
SHEBANGS['bash'] = 'bash'
SHEBANGS['dash'] = 'bash'
SHEBANGS['ksh'] = 'bash'
SHEBANGS['zsh'] = 'zsh'
SHEBANGS['fish'] = 'fish'
SHEBANGS['nu'] = 'nushell'
SHEBANGS['pwsh'] = 'powershell'
SHEBANGS['node'] = 'javascript'
SHEBANGS['nodejs'] = 'javascript'
SHEBANGS['bun'] = 'javascript'
SHEBANGS['deno'] = 'typescript'
SHEBANGS['ts-node'] = 'typescript'
SHEBANGS['tsx'] = 'typescript'
SHEBANGS['ruby'] = 'ruby'
SHEBANGS['perl'] = 'perl'
SHEBANGS['lua'] = 'lua'
SHEBANGS['luajit'] = 'lua'
SHEBANGS['php'] = 'php'
SHEBANGS['elixir'] = 'elixir'
SHEBANGS['escript'] = 'erlang'
SHEBANGS['tclsh'] = 'tcl'
SHEBANGS['wish'] = 'tcl'
SHEBANGS['expect'] = 'tcl'
SHEBANGS['awk'] = 'awk'
SHEBANGS['gawk'] = 'awk'
SHEBANGS['mawk'] = 'awk'
SHEBANGS['julia'] = 'julia'
SHEBANGS['Rscript'] = 'r'
SHEBANGS['racket'] = 'racket'
SHEBANGS['guile'] = 'scheme'
SHEBANGS['chicken'] = 'scheme'
SHEBANGS['sbcl'] = 'commonlisp'
SHEBANGS['clisp'] = 'commonlisp'
SHEBANGS['janet'] = 'janet'
SHEBANGS['fennel'] = 'fennel'
SHEBANGS['nim'] = 'nim'
SHEBANGS['crystal'] = 'crystal'
SHEBANGS['dart'] = 'dart'
SHEBANGS['swift'] = 'swift'
SHEBANGS['groovy'] = 'groovy'
SHEBANGS['scala'] = 'scala'
SHEBANGS['jq'] = 'jq'
SHEBANGS['make'] = 'make'
SHEBANGS['just'] = 'just'
SHEBANGS['zig'] = 'zig'
SHEBANGS['v'] = 'v'
SHEBANGS['rdmd'] = 'd'
SHEBANGS['runghc'] = 'haskell'
SHEBANGS['stack'] = 'haskell'
SHEBANGS['ocaml'] = 'ocaml'
SHEBANGS['emacs'] = 'elisp'
SHEBANGS['gjs'] = 'javascript'
SHEBANGS['osascript'] = 'javascript'


_parsers = {}
_sources = {}
_lines = {}
_trees = {}
_warned = set()


def warn(key, message):
    if key in _warned: return
    _warned.add(key)
    sys.stderr.write(message + '\n')


def parser_for(lang):
    if lang in _parsers: return _parsers[lang]
    parser = None
    try:
        parser = tree_sitter_language_pack.get_parser(lang)
    except Exception as error:
        warn('lang:' + lang, 'inflate: no grammar for %s (%s)' % (lang, error))
    _parsers[lang] = parser
    return parser


def matlab_or_objc(source):
    for marker in (b'@interface', b'@implementation', b'#import', b'@end', b'#include'):
        if marker in source: return 'objc'
    return 'matlab'


def shebang_language(source):
    if not source.startswith(b'#!'): return None
    first = source.split(b'\n', 1)[0].decode('utf-8', 'replace')
    words = first[2:].split()
    if not words: return None
    interpreter = os.path.basename(words[0])
    if interpreter == 'env' and len(words) > 1:
        interpreter = words[1]
        for word in words[1:]:
            if word.startswith('-'): continue
            interpreter = word
            break
    interpreter = re.sub(r'[\d.]+$', '', interpreter)
    if interpreter in SHEBANGS: return SHEBANGS[interpreter]
    return None


def language_for(path):
    """grammar name for a path, sniffing the file only when the name is not enough"""
    name = os.path.basename(path)
    lowered = name.lower()
    if lowered in FILENAMES: return FILENAMES[lowered]
    if name.endswith('.blade.php'): return 'blade'
    if name.endswith('.scm.query'): return 'query'
    root, ext = os.path.splitext(name)
    if ext == '.m':
        source = source_for(path)
        if source is None: return None
        return matlab_or_objc(source)
    if ext in EXTENSIONS: return EXTENSIONS[ext]
    if ext.lower() in EXTENSIONS: return EXTENSIONS[ext.lower()]
    if ext: return None
    source = source_for(path)
    if source is None: return None
    return shebang_language(source)


def source_for(path):
    if path in _sources: return _sources[path]
    data = None
    try:
        with open(path, 'rb') as handle:
            data = handle.read()
    except OSError as error:
        warn('file:' + path, 'inflate: cannot read %s (%s)' % (path, error))
    _sources[path] = data
    return data


def lines_for(path):
    """the source split into rows, cached

    a hit list walks one file many times over, and splitting a megabyte per
    hit is the whole cost of a big `rg | inflate` pipeline.
    """
    if path in _lines: return _lines[path]
    rows = None
    source = source_for(path)
    if source is not None: rows = source.split(b'\n')
    _lines[path] = rows
    return rows


def tree_for(path, lang):
    key = (path, lang)
    if key in _trees: return _trees[key]
    tree = None
    source = source_for(path)
    parser = parser_for(lang)
    if source is not None and parser is not None:
        tree = parser.parse(source)
    _trees[key] = tree
    return tree
