fn helper(value: f32) -> f32 {
    return value + 1.0;
}

fn greet(value: f32) -> f32 {
    return helper(value) * 2.0;
}

fn runner() -> f32 {
    return greet(3.0);
}
