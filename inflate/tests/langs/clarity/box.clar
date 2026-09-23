(define-private (helper (value int))
  (+ value 1))

(define-private (greet (value int))
  (* (helper value) 2))

(define-public (runner)
  (ok (greet 3)))
