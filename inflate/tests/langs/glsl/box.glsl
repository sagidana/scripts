#version 330 core

float helper(float value)
{
    return value + 1.0;
}

float greet(float value)
{
    return helper(value) * 2.0;
}

void runner()
{
    gl_FragDepth = greet(3.0);
}
