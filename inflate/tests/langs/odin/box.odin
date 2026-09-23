package sample

helper :: proc(value: int) -> int {
	return value + 1
}

greet :: proc(value: int) -> int {
	return helper(value) * 2
}

runner :: proc() -> int {
	return greet(3)
}
