package box

helper(value) = out {
	out := value + 1
}

greet(value) = out {
	out := helper(value) * 2
}

runner(value) = out {
	out := greet(value)
}
