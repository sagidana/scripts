package sample

class Box {
    private val size = 1

    fun helper(value: Int): Int {
        return value + size
    }

    fun greet(value: Int): Int {
        return helper(value) * 2
    }

    fun runner(): Int {
        return greet(3)
    }
}
