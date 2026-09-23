<?hh

class Box {
    private int $size = 1;

    public function helper(int $value): int {
        return $value + $this->size;
    }

    public function greet(int $value): int {
        return $this->helper($value) * 2;
    }

    public function runner(): int {
        return $this->greet(3);
    }
}
