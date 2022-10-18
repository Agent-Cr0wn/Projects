#include <math.h>
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string text = get_string("Text: ");

    int letters = 0;
    int words = 0;
    int sentences = 0;

    for (i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }

        else if (text[i] == " ")
        {
            words++;
        }
        else if (text[i] == "." || text[i] == "?" || text[i] == "!")
        {
            sentences++;
        }

    }
    float L = letters / words * 100
    float S = sentences / words * 100

    int index = round(0.0588)

}