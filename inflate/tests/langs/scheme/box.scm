(define (helper value)
  (+ value 1))

(define (greet value)
  (* (helper value) 2))

(define (runner)
  (greet 3))
