function helper(value as Integer) as Integer
    return value + 1
end function

function greet(value as Integer) as Integer
    return helper(value) * 2
end function

function runner() as Integer
    return greet(3)
end function
