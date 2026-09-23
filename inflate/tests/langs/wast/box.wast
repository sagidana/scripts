(module
  (func $helper (param i32) (result i32)
    local.get 0
    i32.const 1
    i32.add)

  (func $greet (param i32) (result i32)
    local.get 0
    call $helper)

  (func $runner (result i32)
    i32.const 3
    call $greet)
)
