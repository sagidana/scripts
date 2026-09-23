extends Node

func helper(value):
	return value + 1

func greet(value):
	return helper(value) * 2

func runner():
	return greet(3)
