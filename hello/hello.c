#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string answer = get_string("What is your name? ");                      //request user's name via input
    printf("Hello, %s\n", answer);                                          //print user's input with hello
}