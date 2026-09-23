local function helper(value: number): number
    return value + 1
end

local function greet(value: number): number
    return helper(value) * 2
end

local function runner(): number
    return greet(3)
end
