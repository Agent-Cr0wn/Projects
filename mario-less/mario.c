#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, x, y, space;
    do
    {
        height = get_int("Height?");
    }
    while(height < 1 || height > 8);

    for(x = 0; x < height; x++)
    {
        for(space = 0; space < height - x - 1; space++)
        {
            printf(" ");
        }
        for(y = 0; y <= x; y++)
        {
            printf("#");
        }
        printf("\n");
    }
}
