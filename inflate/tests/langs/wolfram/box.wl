helper[value_] := Module[{},
  value + 1
]

greet[value_] := Module[{},
  helper[value] * 2
]

runner[] := Module[{},
  greet[3]
]
