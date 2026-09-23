    .text

helper:
    addl $1, %eax
    ret

greet:
    call helper
    addl %eax, %eax
    ret

runner:
    call greet
    ret
