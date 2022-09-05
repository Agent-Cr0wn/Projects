#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string ask = get_string("What is your name? ");
    printf("Hello, %s\n", ask);
}