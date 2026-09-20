struct Widget {
    size: i32,
}

fn helper(value: i32) -> i32 {
    value + 1
}

impl Widget {
    fn grow(&mut self) -> i32 {
        self.size = helper(self.size);
        self.size
    }
}

fn main() {
    let mut w = Widget { size: 3 };
    let bump = |x: i32| helper(x);
    println!("{}", bump(w.grow()));
}
