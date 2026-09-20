(defun helper (value)
  "add one"
  (+ value 1))

(defun grow (size)
  (helper size))

(defun use-widget ()
  (let ((f (lambda (x) (helper x))))
    (funcall f (grow 3))))
