package sample;

class Box {
    public function helper(value:Int):Int {
        return value;
    }

    public function greet(value:Int):Int {
        return helper(value);
    }

    public function runner():Int {
        return greet(3);
    }
}
