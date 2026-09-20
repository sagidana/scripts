_inflate() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    if [[ $cur == -* ]]; then
        COMPREPLY=($(compgen -W '--function --class --callees --callers --root --range --inner --outer --lang --version --help' -- "$cur"))
        return
    fi
    compopt -o default 2>/dev/null
    COMPREPLY=()
}

complete -F _inflate inflate
