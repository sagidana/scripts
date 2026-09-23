namespace Box

def helper (value : Nat) : Nat :=
  value + 1

def greet (value : Nat) : Nat :=
  helper value * 2

def runner : Nat :=
  greet 3

end Box
