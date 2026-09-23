module Box

function helper(value)
    value + 1
end

function greet(value)
    helper(value) * 2
end

function runner()
    greet(3)
end

end
