class Box {
    size = 1

    function helper(value) {
        return value + size
    }

    function greet(value) {
        return helper(value) * 2
    }

    function runner() {
        return greet(3)
    }
}
