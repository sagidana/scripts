function helper
    math $argv[1] + 1
end

function greet
    math (helper $argv[1]) x 2
end

function runner
    greet 3
end
