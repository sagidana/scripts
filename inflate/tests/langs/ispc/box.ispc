int helper(int value)
{
    return value + 1;
}

int greet(int value)
{
    return helper(value) * 2;
}

export void runner(uniform int out[])
{
    out[0] = greet(3);
}
