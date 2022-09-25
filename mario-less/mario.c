#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height, i, j, space;
    do
    {
        height = get_int("Height? ");                                       //request height via input.
    }
    while(height < 1 || height > 8);                                        //only accept input between 1 and 8.

    for(i = 0; i < height; i++)
    {
        for(space = 0; space < height - i - 1; space++)
        {                                                                   //
            printf(" ");
        }
        for(j = 0; j <= i; j++)
        {
            printf("#");                                                    //print "#" in each line equal to number of new lines requested from input
        }
    printf("\n");                                                           //print new line as long as "i" less than height input.
    }
}
