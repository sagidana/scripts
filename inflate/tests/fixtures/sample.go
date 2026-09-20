package main

import "fmt"

type Widget struct {
	Size int
}

func helper(value int) int {
	return value + 1
}

func (w *Widget) Grow() int {
	w.Size = helper(w.Size)
	return w.Size
}

func main() {
	w := &Widget{Size: 3}
	fmt.Println(w.Grow())
}
