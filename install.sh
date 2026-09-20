#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
completions="${XDG_DATA_HOME:-$HOME/.local/share}/bash-completion/completions"
mkdir -p "$completions"
for project in */pyproject.toml; do
    tool=$(dirname "$project")
    pip install "$@" "./$tool"
    ln -sf "$PWD/$tool/completion.bash" "$completions/$tool"
done
echo "completions linked into $completions (loaded by bash-completion in new shells)"
