(ns sample.box)

(defn helper [value]
  (+ value 1))

(defn greet [value]
  (* (helper value) 2))

(defn runner []
  (greet 3))
