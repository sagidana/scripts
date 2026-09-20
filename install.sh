#!/bin/sh
set -e
cd "$(dirname "$0")"
for project in */pyproject.toml; do
    pip install "$@" "./$(dirname "$project")"
done
