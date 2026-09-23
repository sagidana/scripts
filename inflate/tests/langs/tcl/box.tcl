proc helper {value} {
    return [expr {$value + 1}]
}

proc greet {value} {
    return [expr {[helper $value] * 2}]
}

proc runner {} {
    return [greet 3]
}
