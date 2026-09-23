define i32 @helper(i32 %value) {
  %1 = add i32 %value, 1
  ret i32 %1
}

define i32 @greet(i32 %value) {
  %1 = call i32 @helper(i32 %value)
  ret i32 %1
}

define i32 @runner() {
  %1 = call i32 @greet(i32 3)
  ret i32 %1
}
