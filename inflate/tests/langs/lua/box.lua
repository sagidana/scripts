local function helper(value)
    return value + 1
end

local function greet(value)
    return helper(value) * 2
end

local function runner()
    return greet(3)
end
