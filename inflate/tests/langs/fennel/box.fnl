(fn helper [value]
  (+ value 1))

(fn greet [value]
  (* (helper value) 2))

(fn runner []
  (greet 3))
