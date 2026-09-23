package sample;

public class Box {
    private int size = 1;

    public int helper(int value) {
        return value + this.size;
    }

    public int greet(int value) {
        return helper(value) * 2;
    }

    public int runner() {
        return greet(3);
    }
}
