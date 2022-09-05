#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, i, j;
    do
    {
        height = get_int("Height?");
    }
    while(height < 1 || height > 8);

    for(i = 0; i < height; i++)
    {
        for(j = 0; j < height; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
