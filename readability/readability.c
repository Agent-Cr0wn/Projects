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

    for (int i = 0; i < strlen(text); i++)
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
    float L = letters / (float)words * 100;
    float S = sentences / (float)words * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8)

    if (index < 1)
    {
        printf("Before Grade 1");
    }

    else if (index > 16)
    {
        printf("Grade 16+");
    }

    else
    {
        printf("Grade %i", index);
    }
}