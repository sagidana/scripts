local function helper(value: integer): integer
    return value + 1
end

local function greet(value: integer): integer
    return helper(value) * 2
end

local function runner(): integer
    return greet(3)
end
