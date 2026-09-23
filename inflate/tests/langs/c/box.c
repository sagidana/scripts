#include <stdio.h>

int helper(int value)
{
    return value + 1;
}

int greet(int value)
{
    return helper(value) * 2;
}

int runner(void)
{
    return greet(3);
}
