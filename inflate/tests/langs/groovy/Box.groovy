package sample

class Box {
    int size = 1

    int helper(int value) {
        return value + size
    }

    int greet(int value) {
        return helper(value)
    }

    int runner() {
        return greet(3)
    }
}
