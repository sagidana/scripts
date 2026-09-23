package sample

class Box {
  private val size = 1

  def helper(value: Int): Int = {
    value + size
  }

  def greet(value: Int): Int = {
    helper(value) * 2
  }

  def runner(): Int = {
    greet(3)
  }
}
