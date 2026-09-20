#include <stdio.h>

struct widget {
    int size;
};

static int helper(int value)
{
    return value + 1;
}

int grow(struct widget *w)
{
    w->size = helper(w->size);
    return w->size;
}

int main(void)
{
    struct widget w = { 3 };
    printf("%d\n", grow(&w));
    return 0;
}
