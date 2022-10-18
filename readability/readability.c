#include <string.h>
#include <math.h>
#include <ctype.h>
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get User input
    string text = get_string("Text: ");

    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        // Check if input characters have alphabetical value
        if (isalpha(text[i]))
        {
            letters++;
        }

        // Check if input has any spaces
        else if (text[i] == ' ')
        {
            words++;
        }

        // Check if input ends with a bang / interrobang
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }

    }
    // Calculate input value
    float L = letters / (float)words * 100;
    float S = sentences / (float)words * 100;

    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // If the input value is less than 1, return
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    else if (index > 16)
    {
        printf("Grade 16+\n");
    }

    else
    {
        printf("Grade %i\n", index);
    }
}