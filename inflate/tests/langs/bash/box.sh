#!/usr/bin/env bash

helper() {
    echo $(( $1 + 1 ))
}

greet() {
    echo $(( $(helper "$1") * 2 ))
}

runner() {
    greet 3
}
