module 0x1::Box {

    fun helper(value: u64) {
        value;
    }

    fun greet(value: u64) {
        helper(value);
    }

    fun runner() {
        greet(3);
    }
}
