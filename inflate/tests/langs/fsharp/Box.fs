module Box

type Holder() =
    member this.helper(value) =
        value + 1

    member this.greet(value) =
        this.helper(value) * 2

    member this.runner() =
        this.greet(3)
