helper <- function(value) {
  value + 1
}

greet <- function(value) {
  helper(value) * 2
}

runner <- function() {
  greet(3)
}
