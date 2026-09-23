(defun helper (value)
  (+ value 1))

(defun greet (value)
  (* (helper value) 2))

(defun runner ()
  (greet 3))
