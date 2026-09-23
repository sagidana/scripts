DEFINE_FUNCTION INTEGER helper(INTEGER value)
{
    RETURN value + 1
}

DEFINE_FUNCTION INTEGER greet(INTEGER value)
{
    RETURN helper(value) * 2
}

DEFINE_FUNCTION INTEGER runner()
{
    RETURN greet(3)
}
