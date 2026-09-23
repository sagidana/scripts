helper() {
    echo "1"
}

greet() {
    helper
    echo "2"
}

runner() {
    greet
}
