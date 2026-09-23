class Box
  fun helper(value: U32): U32 =>
    value + 1

  fun greet(value: U32): U32 =>
    helper(value) * 2

  fun runner(): U32 =>
    greet(3)
