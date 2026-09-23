module sample

fn helper(value int) int {
	return value + 1
}

fn greet(value int) int {
	return helper(value) * 2
}

fn runner() int {
	return greet(3)
}
