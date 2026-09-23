func helper(value int) int => value + 1

func greet(value int) int =>
  helper(value) * 2

func runner() int =>
  greet(3)
