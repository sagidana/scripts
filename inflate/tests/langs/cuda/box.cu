__device__ int helper(int value)
{
    return value + 1;
}

__global__ void greet(int *out)
{
    out[0] = helper(2);
}

void runner(int *out)
{
    greet<<<1, 1>>>(out);
}
