function(helper value)
    set(result "${value}1")
endfunction()

function(greet value)
    helper("${value}")
endfunction()

function(runner)
    greet("3")
endfunction()
