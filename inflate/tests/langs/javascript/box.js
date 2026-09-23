class Box {
    helper(value) {
        return value + 1;
    }

    greet(value) {
        return this.helper(value) * 2;
    }

    runner() {
        return this.greet(3);
    }
}

module.exports = Box;
