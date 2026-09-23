public class Box {
    private Integer size = 1;

    public Integer helper(Integer value) {
        return value + size;
    }

    public Integer greet(Integer value) {
        return helper(value) * 2;
    }

    public Integer runner() {
        return greet(3);
    }
}
