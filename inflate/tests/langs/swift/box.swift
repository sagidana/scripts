class Box {
    var size = 1

    func helper(_ value: Int) -> Int {
        return value + size
    }

    func greet(_ value: Int) -> Int {
        return helper(value) * 2
    }

    func runner() -> Int {
        return greet(3)
    }
}
