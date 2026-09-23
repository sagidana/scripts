function! helper(value)
    return a:value + 1
endfunction

function! greet(value)
    return helper(a:value) * 2
endfunction

function! runner()
    return greet(3)
endfunction
