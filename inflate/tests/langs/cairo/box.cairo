#[starknet::contract]
mod Box {
    fn helper(value: felt252) -> felt252 {
        value + 1
    }

    fn greet(value: felt252) -> felt252 {
        helper(value) * 2
    }

    fn runner() -> felt252 {
        greet(3)
    }
}
