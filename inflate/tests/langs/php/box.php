<?php

class Box {
    private $size = 1;

    function helper($value) {
        return $value + $this->size;
    }

    function greet($value) {
        return $this->helper($value) * 2;
    }

    function runner() {
        return $this->greet(3);
    }
}
