_each_delegate() {
    local spec
    spec=$(complete -p "$1" 2>/dev/null) || return 1
    local -a parts=($spec)
    local fn='' k
    for (( k = 0; k < ${#parts[@]}; k++ )); do
        case "${parts[k]}" in
            -F) fn=${parts[k + 1]};;
            -o) compopt -o "${parts[k + 1]}" 2>/dev/null;;
        esac
    done
    [[ -n $fn ]] || return 1
    "$fn" "$1" "$2" "$3"
}

_each() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    local cword=$COMP_CWORD
    local -a words=("${COMP_WORDS[@]}")
    local i=1
    while (( i < cword )); do
        case "${words[i]}" in
            -j|--jobs) i=$((i + 2));;
            -j*|--jobs=*|--version) i=$((i + 1));;
            *) break;;
        esac
    done
    if (( i >= cword )) && [[ $cur == -* ]]; then
        COMPREPLY=($(compgen -W '-j --jobs --version --help' -- "$cur"))
        return
    fi
    local start=$i j
    for (( j = i; j < cword; j++ )); do
        case "${words[j]}" in
            '|'|'\|') start=$((j + 1));;
        esac
    done
    if (( start == cword )); then
        COMPREPLY=($(compgen -c -- "$cur"))
        return
    fi
    local cmd=${words[start]}
    local prev=${words[cword - 1]}
    COMP_WORDS=("${words[@]:start}")
    COMP_CWORD=$((cword - start))
    COMP_LINE="${COMP_WORDS[*]}"
    COMP_POINT=${#COMP_LINE}
    if ! _each_delegate "$cmd" "$cur" "$prev" && declare -F _completion_loader >/dev/null; then
        _completion_loader "$cmd"
        _each_delegate "$cmd" "$cur" "$prev"
    fi
    if (( ${#COMPREPLY[@]} == 0 )); then
        compopt -o default 2>/dev/null
        COMPREPLY=()
    fi
}

complete -F _each each
