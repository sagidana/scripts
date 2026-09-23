pub struct Box {
    size: i32,
}

impl Box {
    fn helper(&self, value: i32) -> i32 {
        value + self.size
    }

    fn greet(&self, value: i32) -> i32 {
        self.helper(value) * 2
    }

    fn runner(&self) -> i32 {
        self.greet(3)
    }
}
