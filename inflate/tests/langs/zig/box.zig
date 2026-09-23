const Box = struct {
    size: i32 = 1,

    fn helper(self: Box, value: i32) i32 {
        return value + self.size;
    }

    fn greet(self: Box, value: i32) i32 {
        return self.helper(value) * 2;
    }

    fn runner(self: Box) i32 {
        return self.greet(3);
    }
};
