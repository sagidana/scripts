for _completion in "$(dirname "${BASH_SOURCE[0]}")"/*/completion.bash; do
    source "$_completion"
done
unset _completion
