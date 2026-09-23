#!/usr/bin/env zsh

helper() {
    print $(( $1 + 1 ))
}

greet() {
    print $(( $(helper "$1") * 2 ))
}

runner() {
    greet 3
}
