fn helper(value: Int) -> Int {
  value + 1
}

fn greet(value: Int) -> Int {
  helper(value) * 2
}

pub fn runner() -> Int {
  greet(3)
}
